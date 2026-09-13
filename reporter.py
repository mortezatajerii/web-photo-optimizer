from bidi.algorithm import get_display

from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel

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
# Banner
# =========================================================


def show_banner():
    """
    Display the WEPO application banner.
    """

    banner = r"""
+-----------------------------------------+
|                                         |
|                                         |
|   ██╗    ██╗███████╗██████╗  ██████╗    |
|   ██║    ██║██╔════╝██╔══██╗██╔═══██╗   |
|   ██║ █╗ ██║█████╗  ██████╔╝██║   ██║   |
|   ██║███╗██║██╔══╝  ██╔═══╝ ██║   ██║   |
|   ╚███╔███╔╝███████╗██║     ╚██████╔╝   |
|    ╚══╝╚══╝ ╚══════╝╚═╝      ╚═════╝    |
|                                         |
|                                         |
+-----------------------------------------+
"""

    console.print(
        Text(
            banner,
            style="bold cyan",
            no_wrap=True,
        )
    )

    console.print(
        "Web Image Processing Tool",
        style="bold",
    )

    console.print(
        "Version 1.2.0",
        style="dim",
    )

    console.print()


# =========================================================
# Size Change
# =========================================================


def format_size_change(reduction):
    """
    Format the file size change with a direction indicator.
    """

    if reduction > 0:
        return f"[green]↓ {reduction:.1f}% smaller[/green]"

    if reduction < 0:
        increase = abs(reduction)

        return f"[red]↑ {increase:.1f}% larger[/red]"

    return "[yellow]→ No size change[/yellow]"


# =========================================================
# Processing result
# =========================================================


def show_processing_result(result):
    """
    Display the result of processing a single image.
    """

    input_file = result["input_file"]
    output_file = result["output_file"]

    original_size = result["original_size"]
    output_size = result["output_size"]

    reduction = result["reduction"]

    output_format = result["output_format"].upper()

    console.print(f"[green]✓[/green] {input_file.name}")

    console.print(
        f"  Dimensions: "
        f"{result['original_width']} × "
        f"{result['original_height']} "
        f"→ "
        f"{result['new_width']} × "
        f"{result['new_height']}"
    )

    console.print(
        f"  Size: " f"{format_size(original_size)} " f"→ " f"{format_size(output_size)}"
    )

    console.print(f"  Change: " f"{format_size_change(reduction)}")

    console.print(f"  Output: " f"{output_file.name} " f"({output_format})")

    console.print()


# =========================================================
# Summary
# =========================================================


def show_summary(results, errors):
    """
    Display the final processing summary.
    """

    total = len(results) + len(errors)
    successful = len(results)
    failed = len(errors)

    table = Table(
        title=rtl("Processing Summary"),
        show_header=True,
        header_style="bold",
    )

    table.add_column(
        rtl("Item"),
        justify="right",
    )

    table.add_column(
        rtl("Count"),
        justify="center",
    )

    table.add_row(
        rtl("Total Images"),
        str(total),
    )

    table.add_row(
        rtl("Successful"),
        f"[green]{successful}[/green]",
    )

    table.add_row(
        rtl("Failed"),
        f"[red]{failed}[/red]" if failed else "0",
    )

    console.print()
    console.print(table)

    # Display failed files when processing errors occurred.
    if errors:

        console.print()

        for error in errors:

            console.print(
                Panel(
                    f"[bold]{error['file'].name}[/bold]\n" f"{error['error']}",
                    title=rtl("Error"),
                    border_style="red",
                )
            )


# =========================================================
# File size
# =========================================================


def format_size(size):
    """
    Convert a file size in bytes to a readable format.
    """

    if size < 1024:
        return f"{size} B"

    if size < 1024**2:
        return f"{size / 1024:.1f} KB"

    if size < 1024**3:
        return f"{size / (1024 ** 2):.1f} MB"

    return f"{size / (1024 ** 3):.1f} GB"
