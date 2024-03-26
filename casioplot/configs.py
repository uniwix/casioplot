"""Contains the configurations

All configurations are sotre in the dictionary configs.

:py:func:`_get_config` Serves as an interface
for casioplot.py to get the characters it needs.
"""


from PIL import Image
from os import path

# color type
COLOR = tuple[int, int, int]
# RGB white
_WHITE: COLOR = (255, 255, 255)
# the path for the directory that contains the background images of the configs
_images_directory = path.join(
    path.abspath(path.dirname(__file__)),
    "images"
)

configs = {
    'default': {
        'width': 384,
        'height': 192,
        'left_margin': 0,
        'right_margin': 0,
        'top_margin': 0,
        'bottom_margin': 0,
        'background_image': Image.new('RGB', (384, 192), _WHITE),
        'show_screen': True,
        'save_screen': False,
        'filename': 'casioplot',
        'image_format': 'png'
    },
    'casio_graph_90_plus_e': {
        'width': 384,
        'height': 192,
        'left_margin': 0,
        'right_margin': 0,
        'top_margin': 24,
        'bottom_margin': 0,
        'background_image': Image.open(
            path.join(_images_directory, "CASIO_Graph_90+e_empty.png")
        ).convert('RGB'),
        'show_screen': True,
        'save_screen': False,
        'filename': 'casioplot',
        'image_format': 'png'
    }
}


def _get_config(config: str) -> dict:
    """Gets the settings of a certain config

    :param config: the name of a config, it should be a key of the dictionary configs
    :return: a dictionary where the keys are settings, and the values the values of thouse settings
    """
    if config not in configs.keys():
        raise ValueError(f"No config called {config}")
    return configs[config]
