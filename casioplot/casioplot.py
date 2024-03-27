"""Contains all the functions from ``casioplot`` calculator module.

Available functions:
  - :py:func:`set_pixel`
  - :py:func:`get_pixel`
  - :py:func:`draw_string`
  - :py:func:`clear_screen`
  - :py:func:`show_screen`

You can also use :py:data:`casioplot_settings` to change some behavior.
"""

from typing import Literal
from PIL import Image, ImageTk
import tkinter as tk
from casioplot.configs import _get_config
from casioplot.characters import _get_char

# color type
COLOR = tuple[int, int, int]
# some frequently used colors
_WHITE: COLOR = (255, 255, 255)  # RGB white
_BLACK: COLOR = (0, 0, 0)  # RGBA black
# a list of all settings that if change should trigger the _redraw_screen function
redraw_settings: tuple = ('width', 'height', 'left_margin', 'right_margin', 'top_margin', 'bottom_margin')
# create virtual screen
_screen: Image.Image = Image.new("RGB", (384, 192), _WHITE)
# creates a tkinter window
_window = tk.Tk()
_window.grab_release()
_window.geometry("384x192")
_window.title("casioplot")
_window.attributes("-topmost", True)
# needed to display the screen in the tkinter window
_photo_image = ImageTk.PhotoImage(_screen)
_screen_display = tk.Label(_window, image=_photo_image)
_screen_display.pack()


class Casioplot_settings:
    """Manage casioplot_settings for the casioplot module."""

    def __init__(self) -> None:
        # canvas size
        self.width: int  # canvas width in pixels
        self.height: int  # canvas height in pixels
        # margins
        self.left_margin: int
        self.right_margin: int
        self.top_margin: int
        self.bottom_margin: int
        # background Image
        self.background_image: Image.Image  # some configs like casio_graph_90_plus_e
        # have a special background image
        # Output settings
        self.show_screen: bool  # Show the screen, do not misstake for the functin show_screen()
        self.save_screen: bool  # Save the screen as an image
        # Saving settings
        self.filename: str
        self.image_format: str

        self.config_to('default')  # sets all settings to the default ones


    def _screen_dimensions(self) -> tuple[int, int]:
        """Calculates the dimensions of the screen"""
        return (
            self.left_margin + self.width + self.right_margin,
            self.top_margin + self.height + self.bottom_margin
        )


    def config_to(self, config: str = "default") -> None:
        global _screen, _window
        for setting, value in _get_config(config).items():
            setattr(self, setting, value)

        # a configuration may have a background image
        _screen = self.background_image
        # in case self.show_screen is altered
        if self.show_screen is True:
            _window.deiconify()
        else:
            _window.withdraw()
        # in case the screen dimensions are altered
        screen_width, screen_height = self._screen_dimensions()
        _window.geometry(f"{screen_width}x{screen_height}")


    def set(self, **settings) -> None:
        """Set an attribute for each given setting with the corresponding value."""
        should_redraw_screen: bool = False

        for setting, value in settings.items():
            if getattr(self, setting, None) is None:
                raise AttributeError(f"There is no setting {setting}")

            if setting == 'background_image':
                raise ValueError("you can't set background_image")

            elif setting in redraw_settings:
                should_redraw_screen = True

            elif setting == "show_screen":
                global _window
                if value is True:
                    _window.deiconify()
                else:
                    _window.withdraw()

            setattr(self, setting, value)

        if should_redraw_screen:
            _redraw_screen()


    def get(self, setting: str):
        """Returns an attribute"""
        return getattr(self, setting)


casioplot_settings = Casioplot_settings()


def _redraw_screen() -> None:
    """Redraws _image.

    Only called when casioplot_settings.set() is called,
    used to redraw _image with custom margins, width and height.
    """
    global _screen, _window
    screen_width, screen_height = casioplot_settings._screen_dimensions()

    # Create a new white image
    _screen = Image.new("RGB", (screen_width, screen_height), _WHITE)
    # update the background_image
    casioplot_settings.background_image = _screen
    # updates the window dimensions
    _window.geometry(f"{screen_width}x{screen_height}")


def _coordenates_in_bounds(x: int, y: int) -> bool:
    """Checks if the given coordenates are in bounds of the canvas

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: a bool that says if the given coordenates are in bounds of the canvas
    """
    return 0 <= x < casioplot_settings.get("width") and 0 <= y < casioplot_settings.get("height")


def _canvas_to_screen(x: int, y: int) -> tuple[int, int]:
    """Translates coordenates of the canvas to coordenates in the virtual screen

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The coresponding coordenates in the virtual screen
    """
    return x + casioplot_settings.get("left_margin"), y + casioplot_settings.get("top_margin")


def show_screen() -> None:
    """Show or saves the virtual screen

    This function implement two modes that can be enabled or disabled using the :py:class:`casioplot_settings`:
      - Open the screen as an image (enabled using `casioplot_settings.get('open_image')`).
      - Save the screen to the disk (enabled using `casioplot_settings.get('save_screen')`).
        The image is saved with the filename found in `casioplot_settings.get('filename')`
    """
    if casioplot_settings.get("show_screen") is True:
        global _photo_image, _screen_display, _window
        # show the screen
        _photo_image = ImageTk.PhotoImage(_screen)
        _screen_display["image"] = _photo_image
        _window.update()
    if casioplot_settings.get("save_screen") is True:
        # Save the screen to the disk as an image with the given filename
        _screen.save(
            casioplot_settings.get("filename") + '.' + casioplot_settings.get("image_format"),
            format=casioplot_settings.get("image_format"),
        )


def clear_screen() -> None:
    """Clear the virtual screen."""
    for x in range(casioplot_settings.get('width')):
        for y in range(casioplot_settings.get('height')):
            set_pixel(*_canvas_to_screen(x, y), _WHITE)


def get_pixel(x: int, y: int) -> COLOR | None:
    """Get the RGB color of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the canvas.
    """
    if _coordenates_in_bounds(x, y):
        return _screen.getpixel(_canvas_to_screen(x, y))
    else:
        return None


def set_pixel(x: int, y: int, color: COLOR = _BLACK) -> None:
    """Set the RGB color of the pixel at the given position (from top left)

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255.
    """
    global _screen
    if _coordenates_in_bounds(x, y):
        _screen.putpixel(_canvas_to_screen(x, y), color)


def draw_string(
    x: int,
    y: int,
    text: str,
    color: COLOR = _BLACK,
    size: Literal["small", "medium", "large"] = "medium"
) -> None:
    """Draw a string on the virtual screen with the given RGB color and size.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param text: text that will be drawn
    :param color: The color of the text. A tuple that contain 3 integers from 0 to 255.
    :param size: Size of the text. String from the following values: "small", "medium" or "large".
    :raise ValueError: Raise a ValueError if the size isn't correct.
    """
    def draw_char(x: int, y: int, char_map: tuple, color: COLOR) -> None:
        """Draws a single character

        :param x: x coordinate (from the left)
        :param y: y coordinate (from the top)
        :param char_mpa: a tuple of strings, where every string represents a row
        of the character that is going to be drawn
        :param color: The color of the character
        """
        for y2, row in enumerate(char_map):
            for x2, pixel in enumerate(row):
                if pixel == 'X':
                    set_pixel(x+x2, y+y2, color)

    for char in text:
        if not _coordenates_in_bounds(x, y):
            return

        char_map = _get_char(char, size)
        draw_char(x, y, char_map, color)
        x += len(char_map[0])
