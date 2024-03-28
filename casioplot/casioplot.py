"""Contains all the functions from `casioplot` calculator module.

Available functions:
  - :py:func:`show_screen`
  - :py:func:`clear_screen`
  - :py:func:`set_pixel`
  - :py:func:`get_pixel`
  - :py:func:`draw_string`
"""

import tkinter as tk
from typing import Literal

from PIL import Image, ImageTk

from casioplot.characters import _get_char
from casioplot.configuration_type import configuration
from casioplot.get_config import _get_config_file

# color type
COLOR = tuple[int, int, int]
# some frequently used colors
_WHITE: COLOR = (255, 255, 255)  # RGB white
_BLACK: COLOR = (0, 0, 0)  # RGBA black

# create virtual screen, a proper image will be attributed at the end
_screen: Image.Image = Image.new("RGB", (0, 0))

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

# these two are only used if the setting save_multiple is set to True
save_screen_counter = 0
current_image_number = 1

settings: configuration = _get_config_file("config.toml")


def _screen_dimensions() -> tuple[int, int]:
    """Calculates the dimensions of the screen"""
    return (
        settings["left_margin"] + settings["width"] + settings["right_margin"],
        settings["top_margin"] + settings["height"] + settings["bottom_margin"]
    )


def _setup_screen() -> None:
    """Calculates some screen attributes

    Checks if the margin and size attributes are correctly configured,
    and calculates some settings.
    """
    if hasattr(settings, "background_image"):
        bg_width, bg_height = settings["background_image"].size
        if settings["left_margin"] + settings["right_margin"] >= bg_width:
            raise ValueError("Invalid settings, the combained values of \
                left_margin and right_margin must be smaller than the \
                width of the background image")
        if settings["top_margin"] + settings["bottom_margin"] >= bg_height:
            raise ValueError("Invalid settings, the combained values of \
                top_margin and bottom_margin must be smaller than the \
                height of the background image")

        settings["width"] = bg_width - (settings["left_margin"] + settings["right_margin"])
        settings["height"] = bg_height - (settings["top_margin"] + settings["bottom_margin"])
    else:
        if settings["width"] <= 0:
            raise ValueError("the setting width must be larger than 0")
        if settings["height"] <= 0:
            raise ValueError("the setting height must be larger than 0")

        _redraw_screen()


def _redraw_screen() -> None:
    """Redraws _image.

    Only called when casioplot_settings.set() is called,
    used to redraw _image with custom margins, width and height.
    """
    global _screen, _window

    screen_width, screen_height = _screen_dimensions()
    # Create a new white image
    _screen = Image.new("RGB", (screen_width, screen_height), _WHITE)
    # updates the window dimensions
    _window.geometry(f"{screen_width}x{screen_height}")


# functions only used by the function for the user


def _coordinates_in_bounds(x: int, y: int) -> bool:
    """Checks if the given coordinates are in bounds of the canvas

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: a bool that says if the given coordinates are in bounds of the canvas
    """
    return 0 <= x < settings["width"] and 0 <= y < settings["height"]


def _canvas_to_screen(x: int, y: int) -> tuple[int, int]:
    """Translates coordinates of the canvas to coordinates in the virtual screen

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The corresponding coordinates in the virtual screen
    """
    return x + settings["left_margin"], y + settings["top_margin"]


def save_screen(image_suffix: str = ""):
    """Saves _screen as an image_suffix

    Only used by show_screen
    :param image_suffix: If the setting save_multiple is True existes a need to
    create images with the name `casioplot2.png` for example.
    """
    _screen.save(
        settings["filename"] + image_suffix + '.' + settings["image_format"],
        format=settings["image_format"],
    )


# functions for the user


def show_screen() -> None:
    """Show or saves the virtual screen

    This function implement two modes that can be enabled or disabled using the :py:class:`casioplot_settings`:
      - Open the screen as an image (enabled using `casioplot_settings.get('open_image')`).
      - Save the screen to the disk (enabled using `casioplot_settings.get('save_screen')`).
        The image is saved with the filename found in `casioplot_settings.get('filename')`
    """

    if settings["show_screen"] is True:
        global _photo_image, _screen_display, _window
        # show the screen
        _photo_image = ImageTk.PhotoImage(_screen)
        _screen_display["image"] = _photo_image
        _window.update()

    if settings["save_screen"] is True:
        if settings["save_multiple"] is True:
            global save_screen_counter, current_image_number
            if save_screen_counter == settings["save_rate"]:
                save_screen(str(current_image_number))
                current_image_number += 1
                save_screen_counter = 0

            save_screen_counter += 1
        else:
            # When the program ends, the saved image will show the screen as it was in the last call of show_screen
            save_screen()


def clear_screen() -> None:
    """Clear the virtual screen."""
    for x in range(settings["width"]):
        for y in range(settings["height"]):
            set_pixel(*_canvas_to_screen(x, y), _WHITE)


def get_pixel(x: int, y: int) -> COLOR | None:
    """Get the RGB color of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the canvas.
    """
    if _coordinates_in_bounds(x, y):
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
    if _coordinates_in_bounds(x, y):
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

    def draw_char() -> None:
        """Draws a single character"""
        for y2, row in enumerate(char_map):
            for x2, pixel in enumerate(row):
                if pixel == 'X':
                    set_pixel(x + x2, y + y2, color)

    for char in text:
        if not _coordinates_in_bounds(x, y):
            return

        char_map = _get_char(char, size)
        draw_char()
        x += len(char_map[0])


_setup_screen()
# in case settings["show_screen"] is altered
if settings["show_screen"] is True:
    _window.deiconify()
else:
    _window.withdraw()
# in case the screen dimensions are altered
screen_width, screen_height = _screen_dimensions()
_window.geometry(f"{screen_width}x{screen_height}")
