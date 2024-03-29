import os
import tomllib

from casioplot.configuration_type import configuration

PROJECT_DIR = os.path.curdir
GLOBAL_DIR = os.path.expanduser("~/.config/casioplot")
PRESETS_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "presets"
)
BG_IMAGES_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "bg_images"
)


def _get_first_config_file() -> str:
    """Get the most 'custom' configuration file

    This function returns the most `custom` configuration file in the following order:
    1. casioplot_config.toml file in the directory of the project that is using casiplot
    2. The first toml file in `~/.config/casioplot` directory in alphabetical order
    3. The default configuration file, casioplot/presets/default.toml

    :return: The configuration file path
    """

    # 1
    project_config_file_name = "config.toml"
    project_config_file = os.path.join(PROJECT_DIR, project_config_file_name)
    if os.path.exists(project_config_file):
        return project_config_file

    # 2
    global_config_files = os.listdir(GLOBAL_DIR)
    global_config_files.sort()  # makes sure that the files are in alphabetical order
    if global_config_files == []:
        for file in global_config_files:
            if os.path.splitext(file)[-1] == ".toml":  # see if it is a toml file
                return file

    # 3
    return os.path.join(PRESETS_DIR, "default.toml")


def _get_file_from_preset(preset: str) -> str:
    dir, file_name = preset.split('/')

    if dir == "global":
        return os.path.join(GLOBAL_DIR, file_name)
    elif dir == "presets":
        return os.path.join(PRESETS_DIR, file_name)
    else:
        raise ValueError(f"preset must be global/<file_name> or presets/<file_name> not {dir}/<file_name>")


def _get_image_path(bg_image_setting: str) -> str:
    if "/" not in bg_image_setting:
        path = os.path.join(PROJECT_DIR, bg_image_setting)

    dir, bg_image_name = bg_image_setting.split('/')

    if dir == "global":
        path = os.path.join(GLOBAL_DIR, bg_image_name)
    elif dir == "bg_images":
        path = os.path.join(BG_IMAGES_DIR, bg_image_name)
    else:
        raise ValueError(f"the background image setting can't be {bg_image_setting}, it must be:\
            - <image_name> if it is in the same directory as the configs.py file \n\
            - global/<image_name> if it is the global configs directory \n\
            - bg_images/<image_name> if it is one of the predefined images")

    if os.path.exists(path):
        return path
    else:
        raise ValueError(f"The image {path} doesn't exist")


def _set_settings(toml: dict) -> configuration:
    """Get the settings based on a TOML dictionary.

    :param toml: The TOML dictionary.
    :return: The configuration dictionary.
    """
    if "preset" in toml:
        path = _get_file_from_preset(toml["preset"])
        with open(path, "rb") as source:
            toml2 = tomllib.load(source)
        config = _set_settings(toml2)
    else:
        config = configuration()


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


def _get_settings() -> configuration:
    first_config = _get_first_config_file()
    with open(first_config, "rb") as toml_file:
        toml = tomllib.load(toml_file)
    return _set_settings(toml)
