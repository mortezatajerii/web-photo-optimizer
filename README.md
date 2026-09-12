# WEPO

WEPO is a lightweight offline image optimization tool designed to optimize images for websites by converting and compressing them to WebP.

It provides an interactive terminal interface for batch image processing, allowing users to resize images, configure WebP compression, preserve transparency, remove metadata, and review optimization results.

## Features

* Convert JPEG, PNG, and WebP images to WebP
* Batch image processing
* Resize images while preserving aspect ratio
* Prevent unnecessary image upscaling
* Configurable WebP quality and encoding method
* Preserve image transparency
* Remove image metadata
* Correct image orientation using EXIF information
* Display image dimensions and file size reduction
* Real-time processing progress
* Persistent application settings
* Prevent output filename conflicts
* Continue processing when individual images fail
* Fully offline processing
* Standalone Windows executable support

## How It Works

WEPO processes images through the following workflow:

```text
Input Images
     │
     ▼
Scan Supported Images
     │
     ▼
Orientation Correction
     │
     ▼
Resize if Necessary
     │
     ▼
Remove Metadata
     │
     ▼
Convert & Compress to WebP
     │
     ▼
Save Optimized Images
     │
     ▼
Display Results
```

Original images are never modified. Processed images are saved separately in the `output` directory.

## Supported Formats

### Input

* JPEG (`.jpg`, `.jpeg`)
* PNG (`.png`)
* WebP (`.webp`)

### Output

All processed images are saved as WebP.

## Configuration

WEPO provides configurable image optimization settings:

| Setting               | Description                          |
| --------------------- | ------------------------------------ |
| Maximum Width         | Maximum output image width           |
| Maximum Height        | Maximum output image height          |
| WebP Quality          | WebP compression quality             |
| WebP Method           | WebP encoding method                 |
| Preserve Transparency | Preserve transparency when available |

Settings are stored locally and can be restored to their default values from the application.

## Project Structure

```text
WEPO/
├── main.py
├── cli.py
├── config.py
├── processor.py
├── scanner.py
├── reporter.py
├── WEPO.spec
├── icon.ico
├── requirements.txt
├── .gitignore
├── LICENSE
├── README.md
├── input/
└── output/
```

### Core Modules

* **`main.py`** — Application entry point and workflow orchestration
* **`cli.py`** — Interactive terminal interface and user input
* **`config.py`** — Application settings and configuration management
* **`scanner.py`** — Input image discovery
* **`processor.py`** — Image processing and WebP conversion
* **`reporter.py`** — Processing results, progress, summaries, and errors

## Technologies

* **Python**
* **Pillow** — Image processing and WebP conversion
* **Questionary** — Interactive terminal menus
* **Rich** — Terminal UI, progress indicators, and reporting
* **python-bidi** — Right-to-left text handling in terminal output
* **PyInstaller** — Standalone Windows executable packaging

## Installation

Create a virtual environment and install the required dependencies:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the application with:

```bash
python main.py
```

WEPO automatically creates the required `input` and `output` directories.

Place the images you want to optimize in:

```text
input/
```

Run the application and select the image processing option from the interactive menu.

Optimized WebP images will be saved in:

```text
output/
```

## Windows Executable

WEPO can be packaged as a standalone Windows executable using PyInstaller:

```powershell
pyinstaller WEPO.spec
```

The generated executable will be available in:

```text
dist/WEPO.exe
```

A portable distribution can be structured as:

```text
WEPO-Portable/
├── WEPO.exe
├── input/
├── output/
└── settings.json
```

The packaged application does not require Python to be installed on the target Windows system.

## Development

Run the application directly from the source code:

```bash
python main.py
```

The project currently does not include an automated test suite. Automated testing and CI/CD integration may be added in future versions.

## License

WEPO is licensed under the **GNU General Public License v3.0 or later (GPL-3.0-or-later)**.

See the [`LICENSE`](LICENSE) file for more information.
