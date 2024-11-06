# WePO (Web Photo Optimizer)

WePO is a Python-based tool designed to optimize images for web use. It processes images to reduce their resolution and dimensions while maintaining quality, making them suitable for faster loading times on websites.

## Features

- Batch processing of images
- Converts images to grayscale for mask creation
- Applies binary thresholding to create masks
- Finds and draws contours on images
- Resizes images to specified dimensions
- Saves images with specified DPI using Pillow

## Requirements

- Python 3.11.9
- OpenCV
- NumPy
- Pillow

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mortezatajerii/web-photo-optimizer.git
    cd web-photo-optimizer
    ```

2. Install the required libraries:
    ```bash
    pip install opencv-python-headless numpy Pillow
    ```

## Usage

1. Place your images in the `input_images` directory.
2. Run the script to process the images:
    ```bash
    python wepo.py
    ```

## Example

Here's a simple example of how to use WePO to optimize a single image:

```python
from wepo import optimize_image

input_path = "input_images/example.jpg"
output_path = "output_images/example_optimized.jpg"
optimize_image(input_path, output_path, size=(1024, 1024), dpi=(72, 72))
```
This example demonstrates how to call the optimize_image function to process an image and save the optimized version.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/mortezatajerii/web-photo-optimizer/blob/main/LICENSE) file for details.
