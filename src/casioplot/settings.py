"""Takes care of the settings

Finds the configs files, gets the settings from them and check settings
for wrong settings and config files.
If any of the checks fails the program is terminated.
:file:`casioplot.py` imports the :py:data:`_settings` object from this file.
:py:data:`_settings` contains values for every setting defined in the class :py:class:`Configuration`.
(see :file:`types.py` for more details about :py:class:`Configuration`)
"""

import os
import tomllib

from PIL import Image  # Image.open().size is used to know the dimension of the background image
from casioplot.types import Configuration

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

    This function returns the most 'custom' configuration file in the following order:

    1. :file:`casioplot_config.toml` file in the directory of the project that is using :py:mod:`casioplot`
    2. The first toml file in :file:`~/.config/casioplot` directory in alphabetical order
    3. The default configuration file, :file:`casioplot/presets/default.toml`

    :return: The full configuration file path
    """

    # 1
    # this package may be used in a complex project so the name config.py should not be used
    project_config_file_name = "casioplot_config.toml"
    project_config_file = os.path.join(PROJECT_DIR, project_config_file_name)
    if os.path.exists(project_config_file):
        return project_config_file

    # 2
    if os.path.exists(GLOBAL_DIR) and os.listdir(GLOBAL_DIR) != []:
        global_config_files = os.listdir(GLOBAL_DIR)
        global_config_files.sort()  # makes sure that the files are in alphabetical order

        for file in global_config_files:
            if os.path.splitext(file)[-1] == ".toml":  # see if it is a toml file
                return os.path.join(GLOBAL_DIR, file)

    # 3
    return os.path.join(PRESETS_DIR, "default.toml")


def _get_file_from_pointer(pointer: str) -> str:
    """Translates a default file pointer into a full path for the config file

    :param pointer: The default file pointer, it must be in
                    the format :file:`global/{file_name}` or :file:`presets/{file_name}`
    :return: The full path of the config file
    """
    if "/" not in pointer:
        raise ValueError("Default file pointer must be 'global/<file_name>' or 'presets/<file_name>' \
        not '<file_name>'")

    dir, file_name = pointer.split('/')

    if dir == "global":
        path = os.path.join(GLOBAL_DIR, file_name)
    elif dir == "presets":
        path = os.path.join(PRESETS_DIR, file_name)
    else:
        raise ValueError(f"Default file pointer must be 'global/<file_name>' or 'presets/<file_name>' \
        not '{dir}/<file_name>'")

    if os.path.exists(path):
        return path
    else:
        raise ValueError(f"The config file '{path}' doesn't exist")


def _get_image_path(bg_image_setting: str) -> str:
    """Translates the :python:`setting["background_image"]` to the full path for the image

    :param bg_image_setting: The value of the setting :python:`setting["background_image"]`
    :return: The full path of the image
    """
    if "/" not in bg_image_setting:
        path = os.path.join(PROJECT_DIR, bg_image_setting)

    if bg_image_setting.startswith("global/"):
        path = os.path.join(GLOBAL_DIR, bg_image_setting[7:])
    elif bg_image_setting.startswith("bg_images/"):
        path = os.path.join(BG_IMAGES_DIR, bg_image_setting[10:])
    else:
        raise ValueError(f"The 'background_image' setting can't be '{bg_image_setting}', it must be:\n\
            - '<image_name>' if it is in the same directory as the 'casioplot_configs.py' file \n\
            - 'global/<image_name>' if it is the global configs directory \n\
            - 'bg_images/<image_name>' if it is one of the preset images")


    if os.path.exists(path):
        return path
    else:
        raise ValueError(f"The image '{path}' doesn't exist")


def _get_configuration_from_file(file_path: str) -> tuple[Configuration, str]:
    """Gets the configuration and the default file pointer of a config file from its path

    Preset configuration files like :file:`default.toml` have no default file pointer

    :param file_path: The full path of the config file
    :return: A tuple with the configuration and the default file pointer
    """

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
        "showing_screen": (
            "show_screen",
            "close_window"
        ),
        "saving_screen": (
            "save_screen",
            "image_name",
            "image_format",
            "save_multiple",
            "save_rate"
        )
    }

    def _check_toml(toml: dict) -> None:
        """Checks for wrong settings and section in the toml

        :py:func:`_check_settings` doesn't notice this type of error because:py:func:`_get_configuration_from_file`
        doesn't read them, so they aren't part of the config return by :py:func:`_get_configuration_from_file`
        """
        for section in toml:
            if section == "default_to":  # `default_to` isn't a section
                continue

            # does the section exist?
            if section not in _toml_settings:
                raise ValueError(f"The section '[{section}]' doesn't exist")

            for setting in toml[section]:
                # does the setting exist?
                if setting not in Configuration.__annotations__:
                    raise ValueError(f"The setting '{setting}' doesn't exist")
                # is the setting in the correct section?
                if setting not in _toml_settings[section]:
                    raise ValueError(f"The setting '{setting}' doesn't belong to the section '[{section}]', \
                    it belongs to another section")

    config = Configuration()

    with open(file_path, "rb") as toml_file:
        toml = tomllib.load(toml_file)

    _check_toml(toml)

    if "default_to" in toml:
        pointer = toml["default_to"]
    else:
        pointer = ""

    for section, settings in _toml_settings.items():
        if section in toml:
            for setting in settings:
                if setting in toml[section]:
                    config[setting] = toml[section][setting]
    return config, pointer


def _join_configs(config: Configuration, default_config: Configuration):
    """Adds settings from :py:data:`default_config` to :py:data:`config` if they are missing form :py:data:`config`

    :param config: The current config, the one that will raise an error during the checks
    :param default_config: The configuration from a default file
    """
    for setting in Configuration.__annotations__.keys():
        if setting not in config and setting in default_config:
            config[setting] = default_config[setting]


def _get_settings() -> Configuration:
    """Gets the settings from config files and makes sure that they are correct

    See :py:class:`Configuration` for more details about the settings format that it returns
    See :file:`presets/default.toml` for the default settings and explanations

    :returns: The settings, checked and ready to be used
    """
    current_config_file = _get_first_config_file()
    settings, current_pointer = _get_configuration_from_file(current_config_file)

    while current_pointer != "":
        pointer_is_global: bool = current_pointer.startswith("global/")

        current_config_file = _get_file_from_pointer(current_pointer)
        default_config, current_pointer = _get_configuration_from_file(current_config_file)
        _join_configs(settings, default_config)

        # avoids loops
        if pointer_is_global and not current_pointer.startswith("presets/"):
            raise ValueError("A global config file must not have as default file another global config file \
            , only preset files like 'presets/default' or 'presets/fx-CG50'")

    settings["background_image"] = _get_image_path(settings["background_image"])

    _check_settings(settings)  # avoids running the package with wrong settings

    # Set the settings `width` and `height` to the correct values if a background image is set
    if settings["bg_image_is_set"] is True:
        bg_size_x, bg_size_y = Image.open(settings["background_image"]).size

        settings["width"] = bg_size_x - (settings["left_margin"] + settings["right_margin"])
        settings["height"] = bg_size_y - (settings["top_margin"] + settings["bottom_margin"])

    return settings


def _check_settings(config: Configuration) -> None:
    """Checks if all settings have a value, have the correct type of data and have a proper value.

    Also checks the margins if there is a background image.

    :param config: The settings to be checked
    """

    _settings_value_checks = {
        "width": lambda width: width > 0,
        "height": lambda height: height > 0,
        "left_margin": lambda left_margin: left_margin >= 0,
        "right_margin": lambda right_margin: right_margin >= 0,
        "top_margin": lambda top_margin: top_margin >= 0,
        "bottom_margin": lambda bottom_margin: bottom_margin >= 0,
        "image_format": lambda image_format: image_format in ("jpeg", "jpg", "png", "gif", "bmp", "tiff", "tif"),
        "save_rate": lambda save_rate: save_rate > 0
    }
    """Stores checks for specific settings"""

    _settings_errors = {
        "width": "be greater than zero",
        "height": "be greater than zero",
        "left_margin": "be greater or equal to zero",
        "right_margin": "be greater or equal to zero",
        "top_margin": "be greater or equal to zero",
        "bottom_margin": "be greater or equal to zero",
        "image_format": "be one of the following values, jpeg, jpg, png, gif, bmp, tiff or tif",
        "save_rate": "be greater than zero"
    }
    """Stores the error messages if a check of :py:data:`_settings_value_checks` fails"""

    for setting, correct_type in Configuration.__annotations__.items():
        # does it exist?
        if setting not in config:
            raise ValueError(f"The setting '{setting}' must have a value attributed")

        value = config[setting]

        # does it have the correct type?
        if not isinstance(value, correct_type):
            raise ValueError(f"The setting '{setting}' must be of type '{correct_type}' \
            but the value given is of the type '{type(value)}'")

        # does it have a proper value?
        if setting in _settings_value_checks and not _settings_value_checks[setting](value):
            raise ValueError(f"The settings '{setting}' must '{_settings_errors[setting]}'")

    # some additional checks in case there is a background image
    if config["bg_image_is_set"] is True:
        bg_width, bg_height = Image.open(config["background_image"]).size

        if config["left_margin"] + config["right_margin"] >= bg_width:
            raise ValueError("Invalid settings, the combined values of \
            'left_margin' and 'right_margin' must be smaller than the \
            width of the background image")

        if config["top_margin"] + config["bottom_margin"] >= bg_height:
            raise ValueError("Invalid settings, the combined values of \
            'top_margin' and 'bottom_margin' must be smaller than the \
            height of the background image")


_settings: Configuration = _get_settings()
"""The settings used by the package

:meta hide-value:
"""
