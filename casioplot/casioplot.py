"""Contains all the functions from ``casioplot`` calculator module.

Available functions:
  - :py:func:`set_pixel`
  - :py:func:`get_pixel`
  - :py:func:`draw_string`
  - :py:func:`clear_screen`
  - :py:func:`show_screen`

You can also use :py:data:`settings` to change some behavior.
"""

from os import path
from typing import Literal
from PIL import Image, ImageDraw
from configs import get_config


_WHITE: tuple[int, int, int] = (255, 255, 255)  # RGBA white
_BLACK: tuple[int, int, int] = (0, 0, 0)  # RGBA black

# Create virtual screen
_image: Image.Image = Image.new("RGB", (384, 192), _WHITE)
# Create drawing object (used by the function draw_string
_draw: ImageDraw.ImageDraw = ImageDraw.Draw(_image)


class casioplot_settings:
    """Manage settings for the casioplot module."""

    def __init__(self) -> None:
        # all settings are the default ones
        # Size settings
        self.width: int = 384  # Screen width in pixels
        self.height: int = 192  # Screen height in pixels
        # margins
        self.left_margin: int = 0
        self.right_margin: int = 0
        self.top_margin: int = 0
        self.bottom_margin: int = 0
        # background Image
        self.background_image: Image.Image = Image.new("RGB", (384, 192), _WHITE)
        # Output settings
        self.open_image: bool = False  # Open the screen
        self.save_image: bool = True  # Save the screen as an image
        # Saving settings
        self.filename: str = 'casioplot.png'
        self.image_format: str = 'png'


    def config_to(self, config: str = "default") -> None:
        global _image
        for setting, value in get_config(config).items():
            setattr(self, setting, value)
        _image = self.background_image


    def set(self, **settings) -> None:
        """Set an attribute for each given setting with the corresponding value."""
        for setting, value in settings.items():
            setattr(self, setting, value)
        _redraw_screen()


    def get(self, setting: str):
        """Returns an attribute"""
        return getattr(self, setting)


settings = casioplot_settings()


def _redraw_screen() -> None:
    """Redraws _image.

    Only called when settings.set() is called,
    used to redraw _image with custom margins, width and height.
    """
    global _image, _draw

    # Create a new white image
    _image = Image.new(
        "RGB",
        (
            settings.left_margin + settings.width + settings.right_margin,
            settings.top_margin + settings.height + settings.bottom_margin
        ),
        _WHITE
    )

    settings.background_image = _image

    _draw = ImageDraw.Draw(_image)


def show_screen() -> None:
    """Show or saves the virtual screen

    This function implement two modes that can be enabled or disabled using the :py:class:`settings`:
      - Open the screen as an image (enabled using `settings.get('open_image')`).
      - Save the screen to the disk (enabled using `settings.get('save_image')`).
        The image is saved with the filename found in `settings.get('filename')`
    """
    if settings.get("open_image") is True:
        # open the picture
        _image.show()
    if settings.get("save_image") is True:
        # Save the screen to the disk as an image with the given filename
        _image.save(
            settings.get("filename"),
            format=settings.get("image_format"),
        )


def clear_screen() -> None:
    """Clear the virtual screen."""
    show_screen()
    settings.config_to('default')


def get_pixel(x: int, y: int) -> tuple[int, int, int] | None:
    """Get the RGB color of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the screen.
    """
    if (
        not 0 <= x < settings.get("width")
        or not 0 <= y < settings.get("height")
    ):
        return None
    r: int
    g: int
    b: int
    r, g, b = _image.getpixel(
        (
            x + settings.get("left_margin"),
            y + settings.get("top_margin"),
        )
    )
    return r, g, b


def set_pixel(x: int, y: int, color: tuple[int, int, int] = (0, 0, 0)) -> None:
    """Set the RGB color of the pixel at the given position (from top left)

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255.
    """
    if (
        not 0 <= x < settings.get("width")
        or not 0 <= y < settings.get("height")
    ):
        return
    _image.putpixel(
        (
            x + settings.get("left_margin"),
            y + settings.get("top_margin"),
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
    file_path = path.join(
        path.abspath(path.dirname(__file__)), "chars", size, filename
    )

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
    color: tuple[int, int, int] = (0, 0, 0),
    size: Literal["small", "medium", "large"] = "medium") -> None:
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
