import os
import questionary

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bidi.algorithm import get_display
from questionary import Choice

from reporter import show_banner

console = Console()


# =========================================================
# Screen Manager
# =========================================================


def clear_screen():
    """
    Clear the terminal screen.
    """

    os.system("cls" if os.name == "nt" else "clear")


def start_screen(title=None):
    """
    Start a new terminal screen.
    """

    clear_screen()

    if title:
        console.print()
        console.print(f"[bold]{title}[/bold]")
        console.print()


# =========================================================
# RTL
# =========================================================


def rtl(text):
    """
    Convert RTL text to a display order suitable for terminals
    without proper bidirectional text support.
    """

    # return get_display(text)

    """
    Return text without applying bidirectional text processing.
    """

    return text


# =========================================================
# Main Menu
# =========================================================


def main_menu():
    """
    Display the main menu of WEPO.
    """

    start_screen()

    show_banner()

    return questionary.select(
        rtl("Select an operation:"),
        choices=[
            Choice(
                rtl("Process Images"),
                value="process_images",
            ),
            Choice(
                rtl("Settings"),
                value="settings",
            ),
            Choice(
                rtl("View Settings"),
                value="view_settings",
            ),
            Choice(
                rtl("Reset Settings"),
                value="reset_settings",
            ),
            Choice(
                rtl("Exit"),
                value="exit",
            ),
        ],
        pointer=">",
    ).ask()


# =========================================================
# Settings Menu
# =========================================================


def settings_menu(settings):
    """
    Display the WEPO settings menu.
    """

    start_screen("WEPO Settings")

    return questionary.select(
        rtl("WEPO Settings:"),
        choices=[
            Choice(
                rtl(f"Output Format: " f"{settings['output_format'].upper()}"),
                value="output_format",
            ),
            Choice(
                rtl(f"Maximum Width: {settings['max_width']} px"),
                value="max_width",
            ),
            Choice(
                rtl(f"Maximum Height: {settings['max_height']} px"),
                value="max_height",
            ),
            Choice(
                rtl(f"Quality: {settings['quality']}"),
                value="quality",
            ),
            Choice(
                rtl(f"WebP Encoding Method: " f"{settings['webp_method']}"),
                value="webp_method",
            ),
            Choice(
                rtl(
                    "Preserve Transparency: "
                    f"{'Yes' if settings['preserve_transparency'] else 'No'}"
                ),
                value="preserve_transparency",
            ),
            Choice(
                rtl("Back"),
                value="back",
            ),
        ],
        pointer=">",
    ).ask()


# =========================================================
# Integer Input
# =========================================================


def ask_integer(
    message,
    default,
    minimum=None,
    maximum=None,
):
    """
    Receive and validate an integer value from the user.
    """

    def validate(value):

        value = value.strip()

        if not value.isdigit():
            return rtl("Please enter a valid number.")

        number = int(value)

        if minimum is not None and number < minimum:
            return rtl(f"Value must be at least {minimum}.")

        if maximum is not None and number > maximum:
            return rtl(f"Value must be at most {maximum}.")

        return True

    value = questionary.text(
        rtl(message),
        default=str(default),
        validate=validate,
    ).ask()

    # Keep the current value if the user cancels the input.
    if value is None:
        return default

    return int(value)


# =========================================================
# Output Format
# =========================================================


def ask_output_format(current):
    """
    Ask the user to select the output image format.
    """

    return questionary.select(
        rtl("Select output format:"),
        choices=[
            Choice(rtl("WebP"), value="webp"),
            Choice(rtl("JPEG"), value="jpeg"),
            Choice(rtl("PNG"), value="png"),
        ],
        default=current,
    ).ask()


# =========================================================
# Settings Display
# =========================================================


def show_settings(settings):
    """
    Display the current WEPO settings using Rich.
    """

    start_screen("Current WEPO Settings")

    table = Table(
        title="Current WEPO Settings",
        show_header=True,
        header_style="bold",
    )

    table.add_column(
        rtl("Setting"),
        justify="right",
    )

    table.add_column(
        rtl("Value"),
        justify="left",
    )

    table.add_row(
        rtl("Maximum Width"),
        f"{settings['max_width']} px",
    )

    table.add_row(
        rtl("Maximum Height"),
        f"{settings['max_height']} px",
    )

    table.add_row(
        rtl("Quality"),
        str(settings["quality"]),
    )

    table.add_row(
        rtl("WebP Encoding Method"),
        str(settings["webp_method"]),
    )

    table.add_row(
        rtl("Output Format"),
        settings["output_format"].upper(),
    )

    table.add_row(
        rtl("Preserve Transparency"),
        rtl("Yes" if settings["preserve_transparency"] else "No"),
    )

    console.print()
    console.print(table)
    console.print()


# =========================================================
# Save Settings Confirmation
# =========================================================


def confirm_save_settings():
    """
    Ask the user whether to save the updated settings.
    """

    return questionary.confirm(
        rtl("Save the updated settings?"),
        default=True,
    ).ask()


# =========================================================
# Processing Confirmation
# =========================================================


def confirm_processing(image_count):
    """
    Ask the user whether to start processing.
    """

    return questionary.confirm(
        rtl(f"{image_count} image(s) found. Start processing?"),
        default=True,
    ).ask()


# =========================================================
# Output Folder Action
# =========================================================


def output_folder_action():
    """
    Ask the user how to handle an existing output folder.
    """

    return questionary.select(
        rtl("The output folder is not empty. What would you like to do?"),
        choices=[
            Choice(
                rtl("Clear previous output and start processing"),
                value="clear",
            ),
            Choice(
                rtl("Keep existing files and start processing"),
                value="keep",
            ),
            Choice(
                rtl("Back"),
                value="back",
            ),
        ],
        pointer=">",
    ).ask()


# =========================================================
# Reset Settings Confirmation
# =========================================================


def show_reset_confirmation():
    """
    Ask the user to confirm resetting the settings.
    """

    return questionary.confirm(
        rtl("Reset settings to their default values?"),
        default=False,
    ).ask()


# =========================================================
# Messages
# =========================================================


def show_no_images():
    """
    Display a message when no supported images are found.
    """

    console.print(
        Panel(
            rtl("No supported images were found in the input folder."),
            title="WEPO",
            border_style="yellow",
        )
    )


def show_saved():
    """
    Display a message after the settings are successfully saved.
    """

    console.print(f"[green]✓[/green] {rtl('Settings saved successfully.')}")


def show_reset():
    """
    Display a message after the settings are reset.
    """

    console.print(
        f"[yellow]↺[/yellow] {rtl('Settings reset to their default values.')}"
    )


# =========================================================
# Pause
# =========================================================


def pause():
    """
    Pause execution to let the user review the result.
    """

    questionary.press_any_key_to_continue(rtl("Press any key to continue...")).ask()
