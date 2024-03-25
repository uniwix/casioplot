"""Contains all the functions from ``casioplot`` calculator module.

Available functions:
  - :py:func:`set_pixel`
  - :py:func:`get_pixel`
  - :py:func:`draw_string`
  - :py:func:`clear_screen`
  - :py:func:`show_screen`

You can also use :py:data:`casioplot_settings` to change some behavior.
"""

from os import path
from typing import Literal
from PIL import Image
from configs import get_config


COLOR = tuple[int, int, int]
_WHITE: COLOR = (255, 255, 255)  # RGBA white
_BLACK: COLOR = (0, 0, 0)  # RGBA black

# Create virtual screen
_image: Image.Image = Image.new("RGB", (384, 192), _WHITE)


class Casioplot_casioplot_settings:
    """Manage casioplot_settings for the casioplot module."""

    def __init__(self) -> None:
        # all casioplot_settings are the default ones
        # Size casioplot_settings
        self.width: int = 384  # Screen width in pixels
        self.height: int = 192  # Screen height in pixels
        # margins
        self.left_margin: int = 0
        self.right_margin: int = 0
        self.top_margin: int = 0
        self.bottom_margin: int = 0
        # background Image
        self.background_image: Image.Image = Image.new("RGB", (384, 192), _WHITE)
        # Output casioplot_settings
        self.open_image: bool = False  # Open the screen
        self.save_image: bool = True  # Save the screen as an image
        # Saving casioplot_settings
        self.filename: str = "casioplot.png"
        self.image_format: str = "png"

    def config_to(self, config: str = "default") -> None:
        global _image
        for setting, value in get_config(config).items():
            setattr(self, setting, value)
        _image = self.background_image

    def set(self, **casioplot_settings) -> None:
        """Set an attribute for each given setting with the corresponding value."""
        for setting, value in casioplot_settings.items():
            setattr(self, setting, value)
        _redraw_screen()

    def get(self, setting: str):
        """Returns an attribute"""
        return getattr(self, setting)


casioplot_settings = Casioplot_casioplot_settings()


def _redraw_screen() -> None:
    """Redraws _image.

    Only called when casioplot_settings.set() is called,
    used to redraw _image with custom margins, width and height.
    """
    global _image

    # Create a new white image
    _image = Image.new(
        "RGB",
        (
            casioplot_settings.left_margin + casioplot_settings.width + casioplot_settings.right_margin,
            casioplot_settings.top_margin + casioplot_settings.height + casioplot_settings.bottom_margin,
        ),
        _WHITE,
    )

    casioplot_settings.background_image = _image


def show_screen() -> None:
    """Show or saves the virtual screen

    This function implement two modes that can be enabled or disabled using the :py:class:`casioplot_settings`:
      - Open the screen as an image (enabled using `casioplot_settings.get('open_image')`).
      - Save the screen to the disk (enabled using `casioplot_settings.get('save_image')`).
        The image is saved with the filename found in `casioplot_settings.get('filename')`
    """
    if casioplot_settings.get("open_image") is True:
        # open the picture
        _image.show()
    if casioplot_settings.get("save_image") is True:
        # Save the screen to the disk as an image with the given filename
        _image.save(
            casioplot_settings.get("filename"),
            format=casioplot_settings.get("image_format"),
        )


def clear_screen() -> None:
    """Clear the virtual screen."""
    for x in range(casioplot_settings.get('width')):
        for y in range(casioplot_settings.get('height')):
            set_pixel(x, y, _WHITE)


def get_pixel(x: int, y: int) -> COLOR | None:
    """Get the RGB color of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the screen.
    """
    if not 0 <= x < casioplot_settings.get("width") or not 0 <= y < casioplot_settings.get("height"):
        return None
    r: int
    g: int
    b: int
    r, g, b = _image.getpixel(
        (
            x + casioplot_settings.get("left_margin"),
            y + casioplot_settings.get("top_margin"),
        )
    )
    return r, g, b


def set_pixel(x: int, y: int, color: COLOR = _BLACK) -> None:
    """Set the RGB color of the pixel at the given position (from top left)

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255.
    """
    if not 0 <= x < casioplot_settings.get("width") or not 0 <= y < casioplot_settings.get("height"):
        return
    _image.putpixel(
        (
            x + casioplot_settings.get("left_margin"),
            y + casioplot_settings.get("top_margin"),
        ),
        color,
    )


def _get_filename(character, size: Literal["small", "medium", "large"] = "medium"):
    """Get the file where a character is saved and return the ``space`` file if the character doesn't exist.

    :param character: The character to find
    :param size: The size of the character
    :return: The character filename. A string: "{``./chars`` folder absolute path}/{character}_{size}.png"
    """
    special_chars = {" ": "space"}
    filename = special_chars.get(character, character) + ".txt"
    file_path = path.join(path.abspath(path.dirname(__file__)), "chars", size, filename)

    if not path.isfile(file_path):
        print(f'WARNING: No character "{character}" found for size "{size}".')
        file_path = path.join(
            path.abspath(path.dirname(__file__)), "chars", size, "space.txt"
        )
    return file_path


def draw_string(
    x: int,
    y: int,
    text: str,
    color: COLOR = _BLACK,
    size: Literal["small", "medium", "large"] = "medium",
) -> None:
    """Draw a string on the virtual screen with the given RGB color and size.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param text: text that will be shown
    :param color: The text color. A tuple that contain 3 integers from 0 to 255.
    :param size: Size of the text. String from the following values: "small", "medium" or "large".
    :raise ValueError: Raise a ValueError if the size isn't correct.
    """
    sizes = {"small": (10, 10), "medium": (13, 17), "large": (18, 23)}

    if size not in sizes.keys():
        raise ValueError(
            f'Unknown size "{size}". Size must be one of the following: "small", "medium" or "large"'
        )

    for character in text:
        filename = _get_filename(character, size)
        n = 0
        with open(filename, "r") as c:
            count = 0
            for line in c:
                for j, k in enumerate(line):
                    if k in ["$"]:
                        set_pixel(x + j, y + count, color)
                    n = j
                count += 1
        x += n
