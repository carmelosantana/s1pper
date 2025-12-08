# Custom Top Height - Cura Post-Processing Script
# Stops printing at a custom height while ensuring proper top layers
# Author: carmelosantana for s1pper
# Based on Cura Script API

import re
from ..Script import Script
from UM.Logger import Logger


class CustomTopHeight(Script):
    """
    Post-processing script that stops printing at a specified height
    while ensuring proper top layers (no exposed infill).
    
    How it works:
    - Target Height: The final Z height you want (e.g., 10mm)
    - Top Layers: Number of solid top layers to seal the print (e.g., 5)
    - Result: Prints infill/walls up to (10 - 5*layer_height)mm,
              then prints 5 top layers to reach exactly 10mm
    """

    def getSettingDataString(self):
        return """{
            "name": "Custom Top Height",
            "key": "CustomTopHeight",
            "metadata": {},
            "version": 2,
            "settings": {
                "target_height": {
                    "label": "Target Height (mm)",
                    "description": "Final Z height where the print will stop (including top layers).",
                    "type": "float",
                    "default_value": 50.0,
                    "minimum_value": 0.1,
                    "minimum_value_warning": 1.0,
                    "maximum_value_warning": 300.0,
                    "unit": "mm"
                },
                "top_layers": {
                    "label": "Top Layers",
                    "description": "Number of solid top layers to print. Set to 0 to auto-detect from Cura settings.",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 20
                },
                "layer_height": {
                    "label": "Layer Height (mm)",
                    "description": "Layer height for calculations. Leave at 0 to auto-detect from G-code.",
                    "type": "float",
                    "default_value": 0.0,
                    "minimum_value": 0.0,
                    "maximum_value": 1.0,
                    "unit": "mm"
                },
                "add_message": {
                    "label": "Add Messages",
                    "description": "Add comments to G-code showing where modifications were made.",
                    "type": "bool",
                    "default_value": true
                }
            }
        }"""

    def execute(self, data):
        """Main execution function that processes the G-code."""
        
        # Get settings
        target_height = self.getSettingValueByKey("target_height")
        top_layers_setting = self.getSettingValueByKey("top_layers")
        layer_height_setting = self.getSettingValueByKey("layer_height")
        add_message = self.getSettingValueByKey("add_message")

        Logger.log("d", f"CustomTopHeight: Target height = {target_height}mm")

        # Analyze G-code to find layer information
        layer_info = self._analyze_layers(data)
        
        if not layer_info:
            Logger.log("e", "CustomTopHeight: Could not analyze layer structure")
            return data

        # Determine layer height
        if layer_height_setting > 0:
            layer_height = layer_height_setting
        else:
            layer_height = layer_info.get('layer_height', 0.2)
        
        Logger.log("d", f"CustomTopHeight: Using layer height = {layer_height}mm")

        # Determine number of top layers
        if top_layers_setting > 0:
            top_layers = top_layers_setting
        else:
            top_layers = self._detect_top_layers(data, layer_height)
            if top_layers == 0:
                top_layers = 4  # Safe default
        
        Logger.log("d", f"CustomTopHeight: Using {top_layers} top layers")

        # Calculate heights
        top_layers_height = top_layers * layer_height
        infill_stop_height = target_height - top_layers_height
        
        if infill_stop_height < 0:
            Logger.log("e", f"CustomTopHeight: Target height ({target_height}mm) is less than top layers height ({top_layers_height}mm). Cannot proceed.")
            return data

        Logger.log("d", f"CustomTopHeight: Will print infill/walls up to {infill_stop_height:.2f}mm")
        Logger.log("d", f"CustomTopHeight: Then print {top_layers} top layers from {infill_stop_height:.2f}mm to {target_height:.2f}mm")

        # Find layer indices
        top_layer_start = None  # First layer of the top layers
        final_layer = None      # Last layer at target height
        layers = layer_info.get('layers', [])
        
        for i, layer in enumerate(layers):
            z_height = layer['z']
            
            # Find the first top layer (at or above infill stop height)
            if top_layer_start is None and z_height >= infill_stop_height:
                top_layer_start = i
            
            # Find the final layer at target height
            if z_height >= target_height:
                final_layer = i
                break

        if top_layer_start is None:
            Logger.log("w", "CustomTopHeight: Could not find top layer start. No modifications made.")
            return data
        
        if final_layer is None:
            Logger.log("w", "CustomTopHeight: Target height exceeds print height. No modifications made.")
            return data

        # Calculate which layers to keep: we want exactly 'top_layers' number of layers at the end
        # Count backwards from final_layer to get the right number of top layers
        top_layer_start = max(top_layer_start, final_layer - top_layers + 1)
        
        Logger.log("d", f"CustomTopHeight: Keeping layers 0-{top_layer_start-1}, then printing top layers {top_layer_start}-{final_layer}")

        # Modify G-code
        modified_data = []
        
        for layer_index, layer_data in enumerate(data):
            # Keep all layers before the top layers section
            if layer_index < top_layer_start:
                modified_data.append(layer_data)
            
            # Print the top layers
            elif layer_index >= top_layer_start and layer_index <= final_layer:
                # Add comment on first top layer
                if layer_index == top_layer_start and add_message:
                    message = f";CustomTopHeight: Starting {top_layers} top layers at Z={layers[layer_index]['z']:.2f}mm\n"
                    modified_data.append(message)
                
                modified_data.append(layer_data)
                
                # Add end routine after final layer
                if layer_index == final_layer:
                    if add_message:
                        message = f";CustomTopHeight: Final layer at Z={layers[final_layer]['z']:.2f}mm (target: {target_height}mm)\n"
                        modified_data.append(message)
                    modified_data.append("S__PRINTER_END ; Execute Klipper end macro\n")
                    break
            
            # Stop after final layer
            else:
                break

        Logger.log("i", f"CustomTopHeight: Modified G-code from {len(data)} to {len(modified_data)} layers")
        
        return modified_data

    def _analyze_layers(self, data):
        """Analyze G-code to extract layer information."""
        layers = []
        current_z = None
        previous_z = None
        layer_heights = []

        for layer_index, layer_data in enumerate(data):
            # Look for Z moves
            z_match = re.search(r'G[01]\s+.*Z(\d+\.?\d*)', layer_data, re.IGNORECASE)
            
            if z_match:
                z_value = float(z_match.group(1))
                
                # Track unique Z heights (layers)
                if current_z is None or z_value > current_z:
                    previous_z = current_z
                    current_z = z_value
                    
                    layers.append({
                        'index': layer_index,
                        'z': current_z
                    })
                    
                    # Calculate layer height
                    if previous_z is not None:
                        layer_heights.append(current_z - previous_z)

        # Calculate average layer height
        avg_layer_height = sum(layer_heights) / len(layer_heights) if layer_heights else 0.2

        return {
            'layers': layers,
            'layer_height': avg_layer_height,
            'max_z': current_z
        }

    def _detect_top_layers(self, data, layer_height):
        """Try to detect top layers setting from Cura comments."""
        for layer_data in data[:10]:  # Check first layers for settings
            # Try to find top_layers directly
            match = re.search(r';top_layers\s*=\s*(\d+)', layer_data, re.IGNORECASE)
            if match:
                return int(match.group(1))
            
            # Try to calculate from top_thickness
            match = re.search(r';top_thickness\s*=\s*(\d+\.?\d*)', layer_data, re.IGNORECASE)
            if match:
                thickness = float(match.group(1))
                return max(1, int(round(thickness / layer_height)))
        
        return 0  # Could not detect


# Usage Instructions:
# 1. Copy this file to your Cura scripts folder:
#    - Windows: C:\Program Files\Ultimaker Cura [version]\plugins\PostProcessingPlugin\scripts\
#    - macOS: /Applications/UltiMaker Cura.app/Contents/Resources/plugins/PostProcessingPlugin/scripts/
#    - Linux: ~/.local/share/cura/[version]/scripts/
# 
# 2. Restart Cura
# 
# 3. In Cura, go to: Extensions > Post Processing > Modify G-Code
# 
# 4. Click "Add a script" and select "Custom Top Height"
# 
# 5. Configure:
#    - Target Height: The final Z height where you want the print to stop (e.g., 10mm)
#    - Top Layers: Number of solid top layers to print (0 = auto-detect, default 4)
#    - Layer Height: Your layer height (0 = auto-detect from G-code)
# 
# Example: Target height = 10mm, Top layers = 5, Layer height = 0.2mm
#   - Prints normally from 0mm to ~9mm (45 layers at 0.2mm)
#   - Prints the last 5 layers as top layers from ~9mm to ~10mm
#   - Final print height: ~10mm (exactly as specified)
