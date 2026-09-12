from pathlib import Path

SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def find_images(input_dir):
    return sorted(
        file
        for file in input_dir.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_FORMATS
    )
