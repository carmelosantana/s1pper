# 🥤 s1pper: Ender 3 S1 Pro Macros

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- [Installation](#installation)
  - [Cura Slicer Script Setup](#cura-slicer-script-setup)
  - [Printer Configuration](#printer-configuration)
- [Nozzle Profiles](#nozzle-profiles)
  - [0.4mm Nozzle Profile](#04mm-nozzle-profile)
  - [0.6mm Nozzle Profile](#06mm-nozzle-profile)
- [Macros](#macros)
  - [`BED_MESH_CALIBRATE`](#bed_mesh_calibrate)
  - [`BED_MESH_PURGE_LINE`](#bed_mesh_purge_line)
  - [`S__PRINTER_PREHEAT`](#s__printer_preheat)
  - [`S__PURGE_RESET_POSITION`](#s__purge_reset_position)
  - [`S__START_POSITION`](#s__start_position)
  - [`S__PRINTER_START`](#s__printer_start)
  - [`S__PRINTER_END`](#s__printer_end)
- [Funding](#funding)
- [License](#license)

Enhance your 3D printing experience on the Ender 3 S1 Pro with s1pper macros. These custom macros replace the default Creality and Cura macros, bringing in a dynamic purge line near the mesh area for a smarter, cleaner start to every print.

**Now supports both 0.4mm and 0.6mm nozzle profiles with optimized settings for each!**

## Installation

Follow these steps to get s1pper macros running on your setup:

### Cura Slicer Script Setup

**Install Script:**

1. Download the `KlipperPrintArea.py` file from this repository.
2. Move `KlipperPrintArea.py` to your Cura Slicer scripts folder.

**Update Printer Settings in Cura:**

1. Replace the existing Start G-Code with the following:

```G-Code
S__PRINTER_START EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0} AREA_START=%MINX%,%MINY% AREA_END=%MAXX%,%MAXY%
```

2. Replace the existing End G-Code with the following:

```G-Code
S__PRINTER_END
```

### Printer Configuration

1. Copy the entire `s1pper` folder to your printer's configuration directory
2. Open `printer.cfg` on your printer
3. Add the following line to include s1pper (defaults to 0.4mm nozzle):

```
[include s1pper/s1pper.cfg]
```

4. If using a 0.6mm nozzle, use this instead:

```cfg
[include s1pper/0.6mm/s1pper.cfg]
```

5. Save the file and restart your printer firmware

```G-Code
[include s1pper.cfg]
```

## Nozzle Profiles

This system supports both 0.4mm and 0.6mm nozzles with dedicated optimized settings. The root files (`s1pper.cfg` and `s1pper-automesh.cfg`) load the 0.4mm profile by default.

### Switching Between Nozzles

**To use 0.4mm nozzle (default):**
```
[include s1pper/s1pper.cfg]
```

**To use 0.6mm nozzle:**
```
[include s1pper/0.6mm/s1pper.cfg]
```

### 0.4mm Nozzle Profile

**Default settings for standard 0.4mm nozzles:**
- Default temperatures: 190°C extruder, 60°C bed (material profiles will override as needed)
- Standard flow rate (100%)
- Retraction: 5.0mm (optimized for standard nozzle)
- Pressure advance: 0.04 (balanced for quality and speed)
- Purge line: 15mm extrusion optimized for 0.4mm flow
- Acceleration: 3000mm/s² (standard for quality prints)
- Mesh offset: 5.0mm (standard probing distance)
- Probe samples: 2 per point (balanced speed/accuracy)
- Timelapse support with TIMELAPSE_TAKE_FRAME macro

### 0.6mm Nozzle Profile

**Optimized settings for 0.6mm nozzles:**
- Default temperatures: 190°C extruder, 60°C bed (material profiles will override as needed)
- Flow rate: 90% (reduced to prevent over-extrusion)
- Retraction: 6.5mm (increased for larger nozzle)
- Pressure advance: 0 (disabled to eliminate Y-axis waves)
- Purge line: 20mm extrusion optimized for 0.6mm flow
- Acceleration: 1500mm/s² (reduced for smoother motion)
- Mesh offset: 3.0mm (faster probing)
- Probe samples: 1 per point (optimized for speed)
- 60-second thermal stabilization for cold environments

## Macros

### `BED_MESH_CALIBRATE`

Adapts the original automesh script by ChipCE to accommodate a dynamic purge line near the mesh area, scaling with print size. This macro calculates mesh points based on the print area and ensures an optimized bed mesh calibration for each print.

### `BED_MESH_PURGE_LINE`

Prints a custom purge line near the mesh area to ensure a clean start for every print. This macro dynamically calculates the extrusion length and travel distance based on the print area, aiming to extrude between 5-15mm of filament per pass.

### `S__PRINTER_PREHEAT`

Preheats the printer to the specified or default temperatures - 60°C for the bed and 190°C for the extruder, ensuring readiness for the printing process.

### `S__PURGE_RESET_POSITION`

Resets the extruder position to 0 and elevates the Z-axis to 2.0mm at 3000mm/min, preparing the printer for subsequent operations.

### `S__START_POSITION`

Transitions the printer head to coordinates (X=5, Y=20, Z=0.3) at 5000mm/min, establishing the start position for the purge line.

### `S__PRINTER_START`

A comprehensive start macro that configures the printer for absolute positioning, resets the extruder, homes all axes, preheats the printer, triggers bed mesh calibration within the specified print area, and resets position post-purge.

### `S__PRINTER_END`

A consolidated end macro, amalgamating actions from Creality and Cura with custom tweaks, to gracefully conclude the print job by turning off essential components and repositioning the print head.

## Funding

Discovering value in this project or employing it in a commercial setting? Your generous donation is a stepping stone to continuous improvement and open-source advocacy. 

Here are some avenues to contribute:

- [PayPal](https://www.paypal.com/donate/?business=PWVK9L8VGN4VA&no_recurring=0&item_name=Open+source+advocacy+and+software+development.&currency_code=USD)
- Bitcoin `bc1qhxu9yf9g5jkazy6h4ux6c2apakfr90g2rkwu45`
- Ethereum `0x9f5D6dd018758891668BF2AC547D38515140460f`

Your support is not just a donation, but a testament to the spirit of open-source and the extraordinary things we can achieve together.

## License

The code within this project is licensed under the [MIT License](https://opensource.org/licenses/MIT), *fostering freedom of exploration and adaptation*.

The accompanying documentation is protected by the [CC BY-SA 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/), *promoting sharing and evolution of knowledge*.
