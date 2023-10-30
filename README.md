# 🥤 s1pper: Ender 3 S1 Pro Macros

- [Installation](#installation)
  - [Cura Slicer Script Setup:](#cura-slicer-script-setup)
  - [Printer Configuration:](#printer-configuration)

Enhance your 3D printing experience on the Ender 3 S1 Pro with s1pper macros. These custom macros replace the default Creality and Cura macros, bringing in a dynamic purge line near the mesh area for a smarter, cleaner start to every print.

## Installation

Follow these steps to get s1pper macros running on your setup:

### Cura Slicer Script Setup:

1. **Install Script:**
   - Download the `KlipperPrintArea.py` file from this repository.
   - Move `KlipperPrintArea.py` to your Cura Slicer scripts folder. 

2. **Update Printer Settings in Cura:**
   - **Start G-Code:** Replace the existing Start G-Code with the following:
     ```
     S1PPER_PRINTER_START EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0} AREA_START=%MINX%,%MINY% AREA_END=%MAXX%,%MAXY%
     ```
   - **End G-Code:** Replace the existing End G-Code with the following:
     ```
     S1PPER_PRINTER_END
     ```

### Printer Configuration:

1. **Create s1pper Configuration File:**
   - On your printer's system, create a new file named `s1pper.cfg`.
   - Copy and paste the contents of the `s1pper.cfg` file from this repository into the newly created `s1pper.cfg` on your printer.

2. **Update Klipper Configuration:**
   - Open `printer.cfg` on your printer.
   - Add the following line anywhere in the file:
     ```
     [include s1pper.cfg]
     ```
   - Save the `printer.cfg` file and restart your printer.
