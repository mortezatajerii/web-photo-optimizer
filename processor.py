from io import BytesIO
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
# Image Preparation
# =========================================================


def has_transparency(image):
    """
    Determine whether an image contains transparency information.
    """

    return image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    )


def prepare_image(image, settings, output_format):
    """
    Prepare an image according to the selected output format.
    """

    # Correct the image orientation based on EXIF metadata.
    image = ImageOps.exif_transpose(image)

    # Read original dimensions before processing.
    original_width, original_height = image.size

    transparency = has_transparency(image)

    # -----------------------------------------------------
    # JPEG
    # -----------------------------------------------------

    if output_format == "jpeg":

        # JPEG does not support transparency.
        image = image.convert("RGB")

    # -----------------------------------------------------
    # PNG
    # -----------------------------------------------------

    elif output_format == "png":

        if settings["preserve_transparency"] and transparency:

            # Preserve palette-based transparency when possible.
            if image.mode == "P":
                pass

            elif image.mode == "LA":
                pass

            else:
                image = image.convert("RGBA")

        else:

            # Transparency is not requested.
            if image.mode not in ("1", "L", "P", "RGB"):
                image = image.convert("RGB")

    # -----------------------------------------------------
    # WebP
    # -----------------------------------------------------

    elif output_format == "webp":

        if settings["preserve_transparency"] and transparency:

            image = image.convert("RGBA")

        else:

            image = image.convert("RGB")

    else:

        raise ValueError(f"Unsupported output format: {output_format}")

    # Resize without upscaling.
    image.thumbnail(
        (
            settings["max_width"],
            settings["max_height"],
        ),
        Image.Resampling.LANCZOS,
    )

    return (
        image,
        original_width,
        original_height,
    )


# =========================================================
# WebP Processing
# =========================================================


def save_webp(image, output_file, settings):
    """
    Save an image as WebP using quality-aware encoding.
    """

    quality = settings["quality"]

    if quality >= 100:

        # Use lossless WebP when maximum quality is requested.
        image.save(
            output_file,
            format="WEBP",
            lossless=True,
            quality=100,
            method=settings["webp_method"],
        )

    else:

        # Use lossy WebP only when the user explicitly lowers quality.
        image.save(
            output_file,
            format="WEBP",
            lossless=False,
            quality=quality,
            method=settings["webp_method"],
        )


# =========================================================
# JPEG Processing
# =========================================================


def save_jpeg(image, output_file, settings):
    """
    Save an image as JPEG using the configured quality.
    """

    quality = settings["quality"]

    image.save(
        output_file,
        format="JPEG",
        quality=quality,
        optimize=True,
        subsampling=0 if quality >= 100 else 2,
    )


# =========================================================
# PNG Helpers
# =========================================================


def get_png_transparency(image):
    """
    Return the transparency information required for palette PNGs.
    """

    if image.mode == "P":
        return image.info.get("transparency")

    return None


def encode_png(image):
    """
    Encode an image to PNG in memory without modifying the source image.
    """

    buffer = BytesIO()

    save_kwargs = {
        "format": "PNG",
        "optimize": True,
        "compress_level": 9,
    }

    transparency = get_png_transparency(image)

    if transparency is not None:
        save_kwargs["transparency"] = transparency

    image.save(
        buffer,
        **save_kwargs,
    )

    return buffer.getvalue()


def exact_palette_image(image):
    """
    Create an exact palette representation when the image
    contains no more than 256 unique colors.
    """

    if image.mode not in ("RGB", "RGBA"):
        return None

    try:
        colors = image.getcolors(maxcolors=257)

    except Exception:
        return None

    if colors is None or len(colors) > 256:
        return None

    if image.mode == "RGB":

        return image.quantize(
            colors=len(colors),
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE,
        )

    # RGBA requires Fast Octree in Pillow.
    return image.quantize(
        colors=len(colors),
        method=Image.Quantize.FASTOCTREE,
        dither=Image.Dither.NONE,
    )


# =========================================================
# PNG Lossless Processing
# =========================================================


def save_png_lossless(image, output_file):
    """
    Save PNG using multiple lossless representations
    and keep the smallest valid result.
    """

    candidates = []

    # Candidate 1:
    # Keep the original image representation.
    candidates.append(image)

    # Candidate 2:
    # Use an exact palette when possible.
    palette_image = exact_palette_image(image)

    if palette_image is not None:
        candidates.append(palette_image)

    # Encode all candidates and select the smallest result.
    encoded_candidates = [encode_png(candidate) for candidate in candidates]

    smallest = min(
        encoded_candidates,
        key=len,
    )

    with open(output_file, "wb") as file:
        file.write(smallest)


# =========================================================
# PNG Lossy Processing
# =========================================================


def quantize_png(image, quality):
    """
    Reduce PNG color depth when the user explicitly lowers quality.
    """

    colors = max(
        2,
        min(
            256,
            round(256 * (quality / 100) ** 2),
        ),
    )

    # RGB and L images can use Median Cut.
    if image.mode in ("RGB", "L"):

        return image.quantize(
            colors=colors,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.FLOYDSTEINBERG,
        )

    # RGBA requires Fast Octree.
    if image.mode == "RGBA":

        return image.quantize(
            colors=colors,
            method=Image.Quantize.FASTOCTREE,
            dither=Image.Dither.FLOYDSTEINBERG,
        )

    # Palette images can be quantized directly.
    if image.mode == "P":

        return image.quantize(
            colors=colors,
            dither=Image.Dither.FLOYDSTEINBERG,
        )

    # Normalize unsupported transparency modes.
    if image.mode == "LA":

        rgba = image.convert("RGBA")

        return rgba.quantize(
            colors=colors,
            method=Image.Quantize.FASTOCTREE,
            dither=Image.Dither.FLOYDSTEINBERG,
        )

    return image


def save_png_lossy(image, output_file, settings):
    """
    Save PNG after intentionally reducing color information.
    """

    optimized = quantize_png(
        image,
        settings["quality"],
    )

    data = encode_png(optimized)

    with open(output_file, "wb") as file:
        file.write(data)


def save_png(image, output_file, settings):
    """
    Save PNG using a quality-aware optimization strategy.
    """

    quality = settings["quality"]

    if quality >= 100:

        save_png_lossless(
            image,
            output_file,
        )

    else:

        save_png_lossy(
            image,
            output_file,
            settings,
        )


# =========================================================
# Output Processing
# =========================================================


def save_image(image, output_file, settings):
    """
    Save an image using the selected output format.
    """

    output_format = settings["output_format"]

    if output_format == "webp":

        save_webp(
            image,
            output_file,
            settings,
        )

    elif output_format == "jpeg":

        save_jpeg(
            image,
            output_file,
            settings,
        )

    elif output_format == "png":

        save_png(
            image,
            output_file,
            settings,
        )

    else:

        raise ValueError(f"Unsupported output format: {output_format}")


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

        image, original_width, original_height = prepare_image(
            image,
            settings,
            output_format,
        )

        new_width, new_height = image.size

        # Preserve only essential format-specific information.
        if image.mode == "P":

            transparency = image.info.get("transparency")

            image.info.clear()

            if transparency is not None:
                image.info["transparency"] = transparency

        else:

            # Remove metadata before saving.
            image.info.clear()

        save_image(
            image,
            output_file,
            settings,
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
