from PIL import Image, ImageOps


def get_unique_output_file(output_dir, input_file):
    """
    Generate a unique output filename without overwriting existing files.
    """

    output_file = output_dir / f"{input_file.stem}.webp"

    if not output_file.exists():
        return output_file

    counter = 1

    while True:
        output_file = output_dir / f"{input_file.stem}_{counter}.webp"

        if not output_file.exists():
            return output_file

        counter += 1


def process_image(input_file, output_dir, settings):
    """
    Process a single image and save it as WebP.
    """

    output_file = get_unique_output_file(
        output_dir,
        input_file,
    )

    with Image.open(input_file) as image:

        # Correct the image orientation based on EXIF metadata.
        image = ImageOps.exif_transpose(image)

        # Read the original dimensions before processing.
        original_width, original_height = image.size

        has_alpha = image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        )

        if settings["preserve_transparency"] and has_alpha:
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

        image.save(
            output_file,
            "WEBP",
            quality=settings["webp_quality"],
            method=settings["webp_method"],
        )

    original_size = input_file.stat().st_size
    output_size = output_file.stat().st_size

    reduction = (1 - output_size / original_size) * 100 if original_size > 0 else 0

    return {
        "input_file": input_file,
        "output_file": output_file,
        "original_width": original_width,
        "original_height": original_height,
        "new_width": new_width,
        "new_height": new_height,
        "original_size": original_size,
        "output_size": output_size,
        "reduction": reduction,
    }
