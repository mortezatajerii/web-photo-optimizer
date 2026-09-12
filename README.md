# WEPO

<p align="center">
  <strong>Web Image Optimization & WebP Conversion Tool</strong><br />
  A Python-based offline tool for optimizing website images through resizing, compression, transparency preservation, metadata removal, and WebP conversion.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Pillow-Image%20Processing-3776AB" alt="Pillow" />
  <img src="https://img.shields.io/badge/Rich-Terminal%20UI-FFB000" alt="Rich" />
  <img src="https://img.shields.io/badge/Questionary-Interactive%20CLI-6C63FF" alt="Questionary" />
  <img src="https://img.shields.io/badge/License-GPL--3.0-0A7D8C" alt="License" />
</p>

---

## Table of Contents

* [What is WEPO?](#what-is-wepo)
* [How WEPO Works](#how-wepo-works)
* [Core Processing Rules](#core-processing-rules)
* [Project Philosophy](#project-philosophy)
* [Features](#features)
* [Architecture](#architecture)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Windows Executable](#windows-executable)
* [Development](#development)
* [Testing](#testing)
* [Roadmap](#roadmap)
* [Project Status](#project-status)
* [License](#license)
* [Author](#author)

---

## What is WEPO?

WEPO is a lightweight offline image optimization tool designed specifically for **website image optimization**.

It converts supported images to WebP while reducing file size through configurable resizing and compression. The application also handles common optimization tasks such as EXIF orientation correction, metadata removal, transparency preservation, and output file management.

WEPO is designed for developers, website administrators, and content teams who need a simple local workflow for preparing images before uploading them to a website.

---

## How WEPO Works

WEPO uses an interactive terminal interface to process multiple images from a local input directory.

The processing workflow is:

```text
Input Images
     │
     ▼
Scan Supported Images
     │
     ▼
Correct EXIF Orientation
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
Display Results & Summary
```

Original files are never modified. Optimized files are written separately to the `output` directory.

---

## Core Processing Rules

WEPO follows a small set of predictable processing rules:

* Images are resized only when their dimensions exceed the configured maximum size.
* The original aspect ratio is preserved during resizing.
* Images are never unnecessarily upscaled.
* EXIF orientation is applied before further processing.
* Image metadata is removed before the optimized file is saved.
* Transparency can be preserved for images that contain an alpha channel or transparency information.
* All processed images are saved in WebP format.
* Existing output files are not silently overwritten; a unique filename is generated when necessary.
* A processing error for one image does not stop the remaining images from being processed.
* Original input files remain unchanged throughout the process.

---

## Project Philosophy

WEPO is built around a simple goal:

> **Optimize website images without making the workflow unnecessarily complicated.**

The project focuses on:

* **Simplicity** — An interactive terminal workflow instead of a complex command-line argument system.
* **Predictability** — Clear processing rules and configurable optimization settings.
* **Safety** — Original images are preserved and output filename conflicts are handled automatically.
* **Website-oriented optimization** — The tool is focused on practical image preparation for modern websites rather than general-purpose image editing.
* **Offline processing** — Images are processed locally without requiring an external service.

---

## Features

* Convert JPEG, PNG, and WebP images to WebP
* Batch image processing
* Resize images while preserving aspect ratio
* Prevent unnecessary image upscaling
* Configurable WebP quality
* Configurable WebP encoding method
* Preserve transparency when available
* Remove image metadata
* Correct image orientation using EXIF information
* Display original and optimized dimensions
* Display original and optimized file sizes
* Calculate file size reduction
* Real-time processing progress
* Interactive terminal menus
* Persistent local settings
* Reset settings to defaults
* Prevent output filename conflicts
* Continue processing after individual image failures
* Fully offline processing
* Standalone Windows executable support

---

## Architecture

WEPO follows a simple modular architecture where each component has a focused responsibility.

```text
                    ┌─────────────────┐
                    │     main.py     │
                    │  Application    │
                    │   Orchestration  │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌───────────┐      ┌───────────┐      ┌───────────┐
    │  scanner  │      │ processor │      │ reporter  │
    │    .py    │      │    .py    │      │    .py    │
    └───────────┘      └───────────┘      └───────────┘
                             │
                             ▼
                       ┌───────────┐
                       │  config   │
                       │    .py    │
                       └───────────┘

                       ┌───────────┐
                       │   cli.py  │
                       │ Terminal  │
                       │ Interface │
                       └───────────┘
```

### Core Modules

* **`main.py`** — Application entry point and processing workflow orchestration
* **`cli.py`** — Interactive menus, user input, terminal messages, and output-folder actions
* **`config.py`** — Default settings and persistent configuration management
* **`scanner.py`** — Discovery of supported images inside the input directory
* **`processor.py`** — Image resizing, orientation correction, metadata removal, WebP conversion, and compression
* **`reporter.py`** — Progress display, per-image results, summaries, and error reporting

---

## Technology Stack

* **Python** — Core programming language
* **Pillow** — Image loading, processing, resizing, and WebP conversion
* **Questionary** — Interactive terminal menus and user prompts
* **Rich** — Progress bars, terminal formatting, tables, and reporting
* **python-bidi** — Right-to-left text handling for terminal output
* **PyInstaller** — Packaging the application as a standalone Windows executable

---

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

The `input/` and `output/` directories are created automatically when the application starts if they do not already exist.

---

## Getting Started

WEPO can be used directly from the Python source code or packaged as a standalone Windows executable.

For development and source-based usage, install Python and the project dependencies first.

For end users who prefer a portable application, the project can be packaged with PyInstaller and run without a separate Python installation.

---

## Installation

Create a virtual environment and install the required dependencies.

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

---

## Usage

Run WEPO from the project directory:

```bash
python main.py
```

On startup, WEPO creates the required directories:

```text
input/
output/
```

Place the images you want to optimize inside:

```text
input/
```

Then start the application and select the image processing option from the interactive menu.

Optimized images are saved to:

```text
output/
```

WEPO displays the processing progress and reports the result of each image, including dimensions, file sizes, and reduction percentage.

---

## Configuration

WEPO stores its optimization settings locally.

The current default settings are:

| Setting               | Default | Description                          |
| --------------------- | ------: | ------------------------------------ |
| Maximum Width         |  `1920` | Maximum output width in pixels       |
| Maximum Height        |  `1080` | Maximum output height in pixels      |
| WebP Quality          |    `80` | WebP image quality                   |
| WebP Method           |     `6` | WebP encoding method                 |
| Preserve Transparency |  `True` | Preserve transparency when available |

Settings can be changed from the interactive settings menu and restored to their default values when needed.

In packaged mode, the settings file is stored next to the executable:

```text
WEPO-Portable/
├── WEPO.exe
├── input/
├── output/
└── settings.json
```

---

## Windows Executable

WEPO can be packaged as a standalone Windows executable using PyInstaller.

Build the executable with:

```powershell
pyinstaller WEPO.spec
```

For a clean rebuild:

```powershell
Remove-Item -Recurse -Force build, dist
pyinstaller WEPO.spec
```

The generated executable is located at:

```text
dist/WEPO.exe
```

A portable distribution can then be organized as:

```text
WEPO-Portable/
├── WEPO.exe
├── input/
├── output/
└── settings.json
```

The packaged application does not require Python to be installed on the target Windows machine.

---

## Development

Run WEPO directly from the source code during development:

```bash
python main.py
```

The application is intentionally organized into small modules so that image scanning, processing, configuration, terminal interaction, and reporting can evolve independently.

The project currently uses a sequential processing workflow and does not modify the original input files.

---

## Testing

The current version of WEPO does not include an automated test suite.

Testing is currently performed through manual execution of the application and verification of:

* Image conversion and resizing
* WebP compression results
* Transparency handling
* EXIF orientation correction
* Metadata removal
* Output filename conflict handling
* Processing error recovery
* Configuration persistence
* Windows executable packaging

Automated testing can be introduced in future versions as the project evolves.

---

## Roadmap

Planned improvements may include:

* Automated unit and integration tests
* More advanced image optimization controls
* Additional output and processing options
* Improved reporting and logging
* Additional packaging and distribution improvements
* Optional integrations with website and content-management workflows
* Possible automation and batch-processing enhancements

---

## Project Status

WEPO is an actively evolving personal open-source project focused on practical website image optimization.

The current version provides a functional offline workflow for batch conversion, resizing, compression, metadata removal, transparency preservation, progress reporting, and standalone Windows packaging.

---

## License

WEPO is licensed under the **GNU General Public License v3.0 or later (GPL-3.0-or-later)**.

See the [`LICENSE`](LICENSE) file for more information.

---

## Author

**Morteza**

WEPO is being developed as an ongoing software engineering project focused on building a practical, lightweight, and maintainable tool for optimizing images for modern websites.

