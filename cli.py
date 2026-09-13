import questionary

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bidi.algorithm import get_display
from questionary import Choice

console = Console()


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
    Display and manage WEPO settings.
    """

    while True:

        choice = questionary.select(
            rtl("WEPO Settings:"),
            choices=[
                Choice(
                    rtl(f"Maximum Width: {settings['max_width']} px"),
                    value="max_width",
                ),
                Choice(
                    rtl(f"Maximum Height: {settings['max_height']} px"),
                    value="max_height",
                ),
                Choice(
                    rtl(f"WebP Quality: {settings['webp_quality']}"),
                    value="webp_quality",
                ),
                Choice(
                    rtl(f"WebP Method: {settings['webp_method']}"),
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

        # Return to the previous menu if the user cancels or selects "Back".
        if choice is None or choice == "back":
            return settings

        # ---------------------------------------------
        # Max Width
        # ---------------------------------------------

        if choice == "max_width":
            settings["max_width"] = ask_integer(
                message="Maximum image width:",
                default=settings["max_width"],
                minimum=1,
            )

        # ---------------------------------------------
        # Max Height
        # ---------------------------------------------

        elif choice == "max_height":
            settings["max_height"] = ask_integer(
                message="Maximum image height:",
                default=settings["max_height"],
                minimum=1,
            )

        # ---------------------------------------------
        # WebP Quality
        # ---------------------------------------------

        elif choice == "webp_quality":
            settings["webp_quality"] = ask_integer(
                message="WebP quality:",
                default=settings["webp_quality"],
                minimum=1,
                maximum=100,
            )

        # ---------------------------------------------
        # WebP Method
        # ---------------------------------------------

        elif choice == "webp_method":
            settings["webp_method"] = ask_integer(
                message="WebP encoding method:",
                default=settings["webp_method"],
                minimum=0,
                maximum=6,
            )

        # ---------------------------------------------
        # Transparency
        # ---------------------------------------------

        elif choice == "preserve_transparency":

            result = questionary.confirm(
                rtl("Preserve image transparency?"),
                default=settings["preserve_transparency"],
            ).ask()

            if result is not None:
                settings["preserve_transparency"] = result


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
# Settings Display
# =========================================================


def show_settings(settings):
    """
    Display the current WEPO settings using Rich.
    """

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
        rtl("WebP Quality"),
        str(settings["webp_quality"]),
    )

    table.add_row(
        rtl("WebP Encoding Method"),
        str(settings["webp_method"]),
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
