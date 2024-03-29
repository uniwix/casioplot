import os
import tomllib

from PIL import Image

from casioplot.configuration_type import configuration

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def _get_config_file(file_name: str) -> configuration:
    """Get the configuration file.

    This function searches for the configuration file in the following order:
    1. Absolute path.
    2. The current directory.
    3. The `~/.config/casioplot` directory.
    4. The directory of the package (default configuration files).
    5. The default configuration file.

    :param file_name: The name of the configuration file.
    :return: The configuration file path.
    """

    locations = (
        "",  # 1 and 2
        os.path.expanduser("~/.config/casioplot"),  # 3
        THIS_DIR  # 4
    )

    for loc in locations:
        try:
            path = os.path.join(loc, file_name)
            with open(path, "rb") as source:
                config = tomllib.load(source)
            return _set_settings(config)
        except (IOError, TypeError):
            pass

    # 5
    print(f"[Info] Config file {file_name} not found. Using default configuration.")
    with open(os.path.join(os.path.dirname(__file__), "default.toml"), "rb") as source:
        config = tomllib.load(source)
    return _toml_to_configuration(config, configuration())


def _set_settings(toml: dict) -> configuration:
    """Set the settings based on a TOML dictionary.

    :param toml: The TOML dictionary.
    :return: The configuration dictionary.
    """
    if "preset" in toml:
        config = _get_config_file(toml["preset"])
    else:
        default_file = os.path.join(THIS_DIR, "default.toml")
        with open(default_file, "rb") as source:
            default = tomllib.load(source)
        config = _toml_to_configuration(default, configuration())

    return _toml_to_configuration(toml, config)


_toml_settings = {
    "canvas": (
        "width",
        "height"
    ),
    "margins": (
        "left_margin",
        "right_margin",
        "top_margin",
        "bottom_margin"
    ),
    "background": (
        "bg_image_is_set",
        "background_image"
    ),
    "show_screen": (
        "show_screen"
    ),
    "saving_screen": (
        "save_screen",
        "filename",
        "image_format",
        "save_multiple",
        "save_rate"
    )
}


def _toml_to_configuration(toml: dict, config: configuration) -> configuration:
    """Add the settings from a TOML dictionary to a configuration dictionary.

    :param toml: The TOML dictionary.
    :param config: The configuration dictionary.
    :return: The configuration dictionary with the new settings.
    """

    for section, settings in _toml_settings.items():
        if section in toml:
            for setting in settings:
                if setting in toml[section]:
                    config[setting] = toml[section][setting]

    return config
