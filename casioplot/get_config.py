import os
import tomllib

import imagesize

from casioplot.types import configuration

PROJECT_DIR = os.getcwd()
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
    1. casioplot_config.toml file in the directory of the project that is using casioplot
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
    """Translates a preset into a full path for the file"""
    dir, file_name = preset.split('/')

    if dir == "global":
        path = os.path.join(GLOBAL_DIR, file_name)
    elif dir == "presets":
        path = os.path.join(PRESETS_DIR, file_name)
    else:
        raise ValueError(f"preset must be global/<file_name> or presets/<file_name> not {dir}/<file_name>")

    if os.path.exists(path):
        return path
    else:
        raise ValueError(f"The config file {path} doesn't exist")


def _get_image_path(bg_image_setting: str) -> str:
    """Translates the setting background_image to the full path for the image"""
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
    "background_image": (
        "bg_image_is_set",
        "background_image"
    ),
    "show_screen": (
        "show_screen",
    ),
    "saving_screen": (
        "save_screen",
        "filename",
        "image_format",
        "save_multiple",
        "save_rate"
    )
}


def _get_configuration_from_file(file_path: str) -> tuple[configuration, str]:
    """Gets the configuration and the preset of a config file from it's path

    Preset configuration files like default.toml have no preset
    """
    config = configuration()
    with open(file_path, "rb") as toml_file:
        toml = tomllib.load(toml_file)

    if "preset" in toml:
        preset = toml["preset"]
    else:
        preset = ""

    for section, settings in _toml_settings.items():
        if section in toml:
            for setting in settings:
                if setting == "background_image":
                    config[setting] = _get_image_path(toml[section][setting])
                    config["width"], config["height"] = imagesize.get(config[setting])
                elif setting in toml[section]:
                    config[setting] = toml[section][setting]
    return config, preset


def _join_configs(config: configuration, preset_config: configuration) -> configuration:
    """Adds settings from preset_config to config if they are missing form config"""
    for setting in configuration.__annotations__.keys():
        if setting not in config and setting in preset_config:
            config[setting] = preset_config[setting]

    return config


def _get_settings() -> configuration:
    """Gets the settings from config files"""
    current_config_file = _get_first_config_file()
    config, current_preset = _get_configuration_from_file(current_config_file)

    while current_preset != "":
        preset_is_global: bool = "global/" in current_preset

        current_config_file = _get_file_from_preset(current_preset)
        preset_config, current_preset = _get_configuration_from_file(current_config_file)
        config = _join_configs(config, preset_config)
        print(config)
        # avoids loops
        if preset_is_global and "preset/" not in current_preset:
            raise ValueError("A global config file must not have as preset another global config file\
                , only a preset file like presets/default or presets/fx-CG50")

    # Set correct width and height if a background image is set
    if config["bg_image_is_set"] is True:
        config["width"] = config["width"] - (config["left_margin"] - config["right_margin"])
        config["height"] = config["height"] - (config["top_margin"] - config["bottom_margin"])

    _check_settings(config)  # avoids runing the package with wrong settings

    return config


def _check_settings(settings: configuration) -> None:
    """Checks if all settings have a value, have the correct type of data and have a proper value

    :param settings: The settings to be checked
    """
    print(settings)
    # stores checks for specific settings
    _settings_checks = {
        "width": lambda width: width > 0,
        "height": lambda height: height > 0,
        "left_margin": lambda left_margin: left_margin >= 0,
        "right_margin": lambda right_margin: right_margin >= 0,
        "top_margin": lambda top_margin: top_margin >= 0,
        "bottom_margin": lambda bottom_margin: bottom_margin >= 0,
        "image_format": lambda image_format: image_format in ("jpeg", "jpg", "png", "gif", "bmp", "tiff", "tif"),
        "save_rate": lambda save_rate: save_rate > 0
    }

    # stores the error messages if a check of `_settings_cheks` fails
    _settings_errors = {
        "width": "be greater than zero",
        "height": "be greater than zero",
        "left_margin": "be greater or equal to zero",
        "right_margin": "be greater or equal to zero",
        "top_margin": "be greater or equal to zero",
        "bottom_margin": "be greater or equal to zero",
        "image_format": "be on of the following values, jpeg, jpg, png, gif, bmp, tiff or tif",
        "save_rate": "be greater than zero"
    }

    for setting, correct_type in configuration.__annotations__.items():
        # does it exist?
        if setting not in settings:
            raise ValueError(f"The setting {setting} must have a value attributed")

        value = settings[setting]

        # does it have the correct type?
        if not isinstance(value, correct_type):
            raise ValueError(f"The setting {setting} must be of type {correct_type} \
                but the value given is of the type {type(value)}")
        # does it have a proper value?
        if setting in _settings_checks and not _settings_checks[setting](value):
            raise ValueError(f"The settings {setting} must {_settings_errors[setting]}")

    # some additional checks in case there is a background image
    ## already done by checking height and width
    # if settings["bg_image_is_set"] is True:
    #
    #     if settings["left_margin"] + settings["right_margin"] >= settings["width"]:
    #         raise ValueError("Invalid settings, the combined values of \
    #             left_margin and right_margin must be smaller than the \
    #             width of the background image")
    #     if settings["top_margin"] + settings["bottom_margin"] >= settings["height"]:
    #         raise ValueError("Invalid settings, the combined values of \
    #             top_margin and bottom_margin must be smaller than the \
    #             height of the background image")
