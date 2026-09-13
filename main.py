from pathlib import Path
import shutil

from config import (
    load_settings,
    save_settings,
    reset_settings,
    BASE_DIR,
)
from scanner import find_images
from processor import process_image

from cli import (
    rtl,
    main_menu,
    settings_menu,
    show_settings,
    confirm_save_settings,
    confirm_processing,
    output_folder_action,
    show_no_images,
    show_reset_confirmation,
    show_saved,
    show_reset,
    pause,
)

from reporter import (
    show_banner,
    show_processing_result,
    show_summary,
)

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)

# =========================================================
# Paths
# =========================================================

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# =========================================================
# Directory management
# =========================================================


def prepare_directories():
    """
    Create the required input and output directories.
    """

    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)


def clear_output_directory():
    """
    Remove all files and subdirectories from the output directory.
    """

    for item in OUTPUT_DIR.iterdir():

        if item.is_dir():
            shutil.rmtree(item)

        else:
            item.unlink()


# =========================================================
# Process images
# =========================================================


def process_images(settings):
    """
    Find and process all supported images in the input directory.
    """

    images = find_images(INPUT_DIR)

    if not images:
        show_no_images()
        pause()
        return

    if not confirm_processing(len(images)):
        return

    # Handle existing output files before processing.
    if any(OUTPUT_DIR.iterdir()):

        action = output_folder_action()

        if action is None or action == "back":
            return

        elif action == "clear":
            clear_output_directory()

    results = []
    errors = []

    # Process all images with a visible progress bar.
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:

        task = progress.add_task(
            rtl("Processing images..."),
            total=len(images),
        )

        for input_file in images:

            progress.update(
                task,
                description=rtl(f"Processing: {input_file.name}"),
            )

            try:
                result = process_image(
                    input_file,
                    OUTPUT_DIR,
                    settings,
                )

                results.append(result)

            except Exception as error:

                errors.append(
                    {
                        "file": input_file,
                        "error": str(error),
                    }
                )

            finally:
                progress.advance(task)

    # Display individual results after processing.
    for result in results:
        show_processing_result(result)

    show_summary(
        results=results,
        errors=errors,
    )

    pause()


# =========================================================
# Settings management
# =========================================================


def manage_settings(settings):
    """
    Allow the user to modify and optionally save settings.
    """

    original_settings = settings.copy()

    settings_menu(settings)

    # Ask whether to save the changes only when
    # at least one setting has been modified.

    if settings != original_settings:

        save = confirm_save_settings()

        if save:
            save_settings(settings)
            show_saved()


# =========================================================
# Reset settings
# =========================================================


def reset_user_settings():
    """
    Reset all settings to their default values.
    """

    if not show_reset_confirmation():
        return None

    settings = reset_settings()

    show_reset()
    pause()

    return settings


# =========================================================
# Application
# =========================================================


def main():
    """
    Start and run the WEPO application.
    """

    prepare_directories()

    settings = load_settings()

    show_banner()

    while True:

        choice = main_menu()

        # Exit if the user cancels the menu.
        if choice is None:
            break

        # Process images.
        if choice == "process_images":

            process_images(settings)

        # Manage settings.
        elif choice == "settings":

            manage_settings(settings)

        # Display current settings.
        elif choice == "view_settings":

            show_settings(settings)
            pause()

        # Reset settings.
        elif choice == "reset_settings":

            new_settings = reset_user_settings()

            if new_settings is not None:
                settings = new_settings

        # Exit application.
        elif choice == "exit":

            break


if __name__ == "__main__":
    main()
