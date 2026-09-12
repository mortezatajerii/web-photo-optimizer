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

    return get_display(text)


# =========================================================
# Main Menu
# =========================================================


def main_menu():
    """
    Display the main menu of WEPO.
    """

    return questionary.select(
        rtl("عملیات موردنظر را انتخاب کنید:"),
        choices=[
            Choice(
                rtl("پردازش تصاویر"),
                value="پردازش تصاویر",
            ),
            Choice(
                rtl("تنظیمات"),
                value="تنظیمات",
            ),
            Choice(
                rtl("مشاهده تنظیمات"),
                value="مشاهده تنظیمات",
            ),
            Choice(
                rtl("بازنشانی تنظیمات"),
                value="بازنشانی تنظیمات",
            ),
            Choice(
                rtl("خروج"),
                value="خروج",
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
            rtl("تنظیمات WEPO:"),
            choices=[
                Choice(
                    rtl(f"حداکثر عرض: {settings['max_width']} px"),
                    value="max_width",
                ),
                Choice(
                    rtl(f"حداکثر ارتفاع: {settings['max_height']} px"),
                    value="max_height",
                ),
                Choice(
                    rtl(f"کیفیت WebP: {settings['webp_quality']}"),
                    value="webp_quality",
                ),
                Choice(
                    rtl(f"روش فشرده سازی WebP: {settings['webp_method']}"),
                    value="webp_method",
                ),
                Choice(
                    rtl(
                        "حفظ شفافیت: "
                        f"{'بله' if settings['preserve_transparency'] else 'خیر'}"
                    ),
                    value="preserve_transparency",
                ),
                Choice(
                    rtl("بازگشت"),
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
                message="حداکثر عرض تصویر:",
                default=settings["max_width"],
                minimum=1,
            )

        # ---------------------------------------------
        # Max Height
        # ---------------------------------------------

        elif choice == "max_height":
            settings["max_height"] = ask_integer(
                message="حداکثر ارتفاع تصویر:",
                default=settings["max_height"],
                minimum=1,
            )

        # ---------------------------------------------
        # WebP Quality
        # ---------------------------------------------

        elif choice == "webp_quality":
            settings["webp_quality"] = ask_integer(
                message="کیفیت WebP:",
                default=settings["webp_quality"],
                minimum=1,
                maximum=100,
            )

        # ---------------------------------------------
        # WebP Method
        # ---------------------------------------------

        elif choice == "webp_method":
            settings["webp_method"] = ask_integer(
                message="روش فشرده سازی WebP:",
                default=settings["webp_method"],
                minimum=0,
                maximum=6,
            )

        # ---------------------------------------------
        # Transparency
        # ---------------------------------------------

        elif choice == "preserve_transparency":

            result = questionary.confirm(
                rtl("آیا شفافیت تصاویر حفظ شود؟"),
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
            return rtl("لطفاً یک عدد معتبر وارد کنید.")

        number = int(value)

        if minimum is not None and number < minimum:
            return rtl(f"مقدار باید حداقل {minimum} باشد.")

        if maximum is not None and number > maximum:
            return rtl(f"مقدار باید حداکثر {maximum} باشد.")

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
        title="تنظیمات فعلی WEPO",
        show_header=True,
        header_style="bold",
    )

    table.add_column(
        rtl("تنظیم"),
        justify="right",
    )

    table.add_column(
        rtl("مقدار"),
        justify="left",
    )

    table.add_row(
        rtl("حداکثر عرض"),
        f"{settings['max_width']} px",
    )

    table.add_row(
        rtl("حداکثر ارتفاع"),
        f"{settings['max_height']} px",
    )

    table.add_row(
        rtl("کیفیت WebP"),
        str(settings["webp_quality"]),
    )

    table.add_row(
        rtl("روش فشرده سازی WebP"),
        str(settings["webp_method"]),
    )

    table.add_row(
        rtl("حفظ شفافیت"),
        rtl("بله" if settings["preserve_transparency"] else "خیر"),
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
        rtl("تغییرات تنظیمات ذخیره شوند؟"),
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
        rtl(f"{image_count} تصویر پیدا شد. پردازش شروع شود؟"),
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
        rtl("پوشه خروجی خالی نیست. چه کاری انجام شود؟"),
        choices=[
            Choice(
                rtl("پاک کردن خروجی قبلی و شروع پردازش"),
                value="clear",
            ),
            Choice(
                rtl("حفظ فایل های قبلی و شروع پردازش"),
                value="keep",
            ),
            Choice(
                rtl("بازگشت"),
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
        rtl("تنظیمات به حالت اصلی بازگردانده شوند؟"),
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
            rtl("هیچ تصویر پشتیبانی شده ای در پوشه input پیدا نشد."),
            title="WEPO",
            border_style="yellow",
        )
    )


def show_saved():
    """
    Display a message after the settings are successfully saved.
    """

    console.print(f"[green]✓[/green] {rtl('تنظیمات با موفقیت ذخیره شدند.')}")


def show_reset():
    """
    Display a message after the settings are reset.
    """

    console.print(f"[yellow]↺[/yellow] {rtl('تنظیمات به حالت اصلی بازگردانده شدند.')}")


# =========================================================
# Pause
# =========================================================


def pause():
    """
    Pause execution to let the user review the result.
    """

    questionary.press_any_key_to_continue(rtl("برای ادامه یک کلید فشار دهید...")).ask()
