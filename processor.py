from PIL import Image, ImageOps

# =========================================================
# Output Format Configuration
# =========================================================

FORMAT_CONFIG = {
    "webp": {
        "extension": ".webp",
        "pillow_format": "WEBP",
    },
    "jpeg": {
        "extension": ".jpg",
        "pillow_format": "JPEG",
    },
    "png": {
        "extension": ".png",
        "pillow_format": "PNG",
    },
}


# =========================================================
# Output File
# =========================================================


def get_unique_output_file(output_dir, input_file, extension):
    """
    Generate a unique output filename without overwriting existing files.
    """

    output_file = output_dir / f"{input_file.stem}{extension}"

    if not output_file.exists():
        return output_file

    counter = 1

    while True:

        output_file = output_dir / f"{input_file.stem}_{counter}{extension}"

        if not output_file.exists():
            return output_file

        counter += 1


# =========================================================
# Image Processing
# =========================================================


def process_image(input_file, output_dir, settings):
    """
    Process a single image using the selected output format.
    """

    output_format = settings["output_format"]

    if output_format not in FORMAT_CONFIG:
        raise ValueError(f"Unsupported output format: {output_format}")

    format_config = FORMAT_CONFIG[output_format]

    output_file = get_unique_output_file(
        output_dir,
        input_file,
        format_config["extension"],
    )

    with Image.open(input_file) as image:

        # Correct the image orientation based on EXIF metadata.
        image = ImageOps.exif_transpose(image)

        # Read the original dimensions before processing.
        original_width, original_height = image.size

        has_alpha = image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        )

        # JPEG does not support transparency.
        if settings["preserve_transparency"] and has_alpha and output_format != "jpeg":
            image = image.convert("RGBA")

        else:
            image = image.convert("RGB")

        image.thumbnail(
            (
                settings["max_width"],
                settings["max_height"],
            ),
            Image.Resampling.LANCZOS,
        )

        new_width, new_height = image.size

        # Remove all image metadata before saving.
        image.info.clear()

        # ---------------------------------------------
        # WebP
        # ---------------------------------------------

        if output_format == "webp":

            image.save(
                output_file,
                format="WEBP",
                quality=settings["quality"],
                method=settings["webp_method"],
            )

        # ---------------------------------------------
        # JPEG
        # ---------------------------------------------

        elif output_format == "jpeg":

            image.save(
                output_file,
                format="JPEG",
                quality=settings["quality"],
                optimize=True,
            )

        # ---------------------------------------------
        # PNG
        # ---------------------------------------------

        elif output_format == "png":

            image.save(
                output_file,
                format="PNG",
                optimize=True,
            )

    original_size = input_file.stat().st_size
    output_size = output_file.stat().st_size

    reduction = (1 - output_size / original_size) * 100 if original_size > 0 else 0

    return {
        "input_file": input_file,
        "output_file": output_file,
        "output_format": output_format,
        "original_width": original_width,
        "original_height": original_height,
        "new_width": new_width,
        "new_height": new_height,
        "original_size": original_size,
        "output_size": output_size,
        "reduction": reduction,
    }
