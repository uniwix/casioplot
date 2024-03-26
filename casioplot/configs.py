from PIL import Image
from os import path

_WHITE: tuple[int, int, int] = (255, 255, 255)  # RGBA white
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


def get_config(config: str) -> dict:
    if config not in configs.keys():
        raise ValueError(f"No config called {config}")
    return configs[config]
