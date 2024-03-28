"""Contains some preset configurations

All preset configurations are stored in the dictionary configs.

:py:func:`_get_config` Serves as an interface
for casioplot.py to get the preset configurations it needs.
"""

from PIL import Image
import os

from casioplot.configuration_type import configuration


images_directory = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "images"
)

configs: dict[str, configuration] = {
    "default": {
        "width": 384,
        "height": 192,
        "left_margin": 0,
        "right_margin": 0,
        "top_margin": 0,
        "bottom_margin": 0,
        "bg_image_is_set": False,
        "background_image": Image.new("RGB", (0, 0)),
        "show_screen": True,
        "save_screen": False,
        "filename": "casioplot",
        "image_format": "png",
        "save_multiple": False,
        "save_rate": 0
    },
    "fx-CG50": {
        "width": 384,
        "height": 192,
        "left_margin": 8,
        "right_margin": 8,
        "top_margin": 26,
        "bottom_margin": 10,
        "bg_image_is_set": True,
        "background_image": Image.open(os.path.join(images_directory, "calculator.png")),
        "show_screen": True,
        "save_screen": False,
        "filename": "casioplot",
        "image_format": "png",
        "save_multiple": False,
        "save_rate": 0
    },
}
# this options only exist for better user experience
configs["fx-CG50 AU"] = configs["fx-CG50"]
configs["graph 90+e"] = configs["fx-CG50"]


def _get_config(config: str) -> configuration:
    """Gets the settings of a certain config

    :param config: the name of a configuration, it should be a key of the dictionary configs
    :return: a preset configuration
    """
    if config not in configs.keys():
        raise ValueError(f"No config called {config}")
    return configs[config]
