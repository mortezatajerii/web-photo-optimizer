from pathlib import Path
import copy
import json
import sys


def get_base_dir():
    """
    Return the directory where the application executable is located.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


BASE_DIR = get_base_dir()
SETTINGS_FILE = BASE_DIR / "settings.json"

# Default application settings
DEFAULT_SETTINGS = {
    "max_width": 1920,
    "max_height": 1080,
    "quality": 80,
    "webp_method": 6,
    "preserve_transparency": True,
    "output_format": "webp",
}


def load_settings():
    """
    Load settings from settings.json.

    Missing or invalid settings fall back to the default values.
    """

    if not SETTINGS_FILE.exists():
        return copy.deepcopy(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)

        settings = copy.deepcopy(DEFAULT_SETTINGS)
        settings.update(saved)

        return settings

    except (json.JSONDecodeError, OSError):
        return copy.deepcopy(DEFAULT_SETTINGS)


def save_settings(settings):
    """
    Save the current settings to settings.json.
    """

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            settings,
            file,
            ensure_ascii=False,
            indent=4,
        )


def reset_settings():
    """
    Reset all settings to their default values and save them.
    """

    settings = copy.deepcopy(DEFAULT_SETTINGS)
    save_settings(settings)
    return settings
