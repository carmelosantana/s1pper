# 🥤 s1pper: Ender 3 S1 Pro Macros

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- [Installation](#installation)
  - [Cura Slicer Script Setup](#cura-slicer-script-setup)
  - [Printer Configuration](#printer-configuration)
- [Features](#features)
- [Macros](#macros)
  - [`BED_MESH_CALIBRATE`](#bed_mesh_calibrate)
  - [`BED_MESH_PURGE_LINE`](#bed_mesh_purge_line)
  - [`S__PRINTER_PREHEAT`](#s__printer_preheat)
  - [`S__PURGE_RESET_POSITION`](#s__purge_reset_position)
  - [`S__START_POSITION`](#s__start_position)
  - [`S__PRINTER_START`](#s__printer_start)
  - [`S__PRINTER_END`](#s__printer_end)
- [Configuration](#configuration)
  - [Pressure Advance](#pressure-advance)
  - [Customizing Settings](#customizing-settings)
- [Funding](#funding)
- [License](#license)

Enhance your 3D printing experience on the Ender 3 S1 Pro with s1pper macros. These custom macros replace the default Creality and Cura macros, bringing in adaptive bed mesh calibration and a dynamic purge line that scales with your print size for a smarter, cleaner start to every print.

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
3. Add the following line to include s1pper macros:

```cfg
[include s1pper/s1pper.cfg]
```

4. Save the file and restart your printer firmware

## Features

**Adaptive Bed Mesh Calibration:**
- Dynamic mesh probing based on actual print area (saves time on small prints)
- Configurable mesh offset (5.0mm default, adjustable in macro)
- Probe count scales with print size (minimum 4x4, configurable)
- Supports both bicubic and lagrange algorithms
- 2 samples per probe point for accuracy (adjustable)

**Intelligent Purge Line:**
- Dynamically scales to 1.5x your print area height
- Minimum 50mm purge ensures adequate priming
- Automatically capped at bed maximum (220mm Y-axis)
- Proportional extrusion based on purge length
- Starts near print area for efficient workflow
- Dual-pass purge for consistent flow

**Smart Print Start Sequence:**
1. Homes all axes
2. Preheats bed and extruder to target temperatures
3. Performs adaptive mesh calibration for print area
4. Executes dynamic purge line
5. Resets extruder position and Z-height
6. Ready to print!

**Configuration:**
- Pressure advance enabled (0.04 default, tunable)
- Default temperatures: 190°C extruder / 60°C bed
- Material profiles from slicer override defaults
- Works with Cura's KlipperPrintArea.py script

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

## Configuration

### Pressure Advance

Pressure advance is enabled by default in `printer.cfg` with a starting value of `0.04`. This helps compensate for pressure buildup in the nozzle during direction changes, improving corner quality.

**To calibrate pressure advance for your specific filament:**

1. Print a calibration test using the `TUNING_TOWER` command:

```gcode
TUNING_TOWER COMMAND=SET_PRESSURE_ADVANCE PARAMETER=ADVANCE START=0 FACTOR=.005
```

2. Examine the test print to find where corners look best
3. Calculate the optimal value: `pressure_advance = start + (height_of_best_layer * factor)`
4. Update the value in your `printer.cfg` under `[extruder]`:

```cfg
pressure_advance: 0.04  # Replace with your calibrated value
```

5. Save and restart Klipper

**Typical ranges:**
- Direct drive extruders: 0.02 - 0.08
- Bowden extruders: 0.30 - 0.70

### Customizing Settings

You can customize various parameters in the macro files:

**In `s1pper-automesh.cfg`:**
- `mesh_area_offset`: Clearance between print area and probe area (default: 5.0mm)
- `probe_samples`: Number of samples per probe point (default: 2)
- `min_probe_count`: Minimum mesh points (default: 4x4)
- `probe_count_scale_factor`: Scales probe density (default: 1.5)
- `min_purge_length`: Minimum purge line length (default: 50mm)

**In `s1pper.cfg`:**
- Default temperatures in `S__PRINTER_PREHEAT`
- Start position coordinates in `S__START_POSITION`
- End position and retraction in `S__PRINTER_END`

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
