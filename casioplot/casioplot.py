"""Contains all the functions from `casioplot` calculator module.

Available functions:
  - :py:func:`show_screen`
  - :py:func:`clear_screen`
  - :py:func:`set_pixel`
  - :py:func:`get_pixel`
  - :py:func:`draw_string`

Contains the original functions from the `casioplot` calculator module and the code needed to emulate the screen.
"""

import tkinter as tk
from typing import Literal

from casioplot.characters import _get_char
from casioplot.settings import _settings
from casioplot.types import Color
from casioplot.utils import _coordinates_in_bounds, _save_screen, _color_tuple_to_hex, _canvas_to_screen

# some frequently used colors
_WHITE: Color = (255, 255, 255)  # RGB white
_BLACK: Color = (0, 0, 0)  # RGBA black

# these two are only used if the setting save_multiple is set to True
save_screen_counter = 0
current_image_number = 1


# functions for the user

def show_screen() -> None:
    """Show or saves the virtual screen

    This function implement two modes that can be enabled or disabled using the :py:class:`casioplot_settings`:
      - show the screen as an image, if `show_screen` is True
      - Save the screen to the disk, if `save_screen` in True
        The image is saved with the filename found in `filename`
    """

    if _settings["show_screen"] is True:
        # show the screen
        _window.update()

    if _settings["save_screen"] is True:
        if _settings["save_multiple"] is True:
            global save_screen_counter, current_image_number
            if save_screen_counter == _settings["save_rate"]:
                _save_screen(_screen, _settings["filename"], _settings["image_format"], str(current_image_number))
                current_image_number += 1
                save_screen_counter = 0

            save_screen_counter += 1
        else:
            # When the program ends, the saved image will show the screen as it was in the last call of show_screen
            _save_screen(_screen, _settings["filename"], _settings["image_format"])


def clear_screen() -> None:
    """Clear the virtual screen"""
    _screen.put(
        "white",
        to=(
            _settings["left_margin"],
            _settings["top_margin"],
            _settings["left_margin"] + _settings["width"],
            _settings["top_margin"] + _settings["height"]
        )
    )


def get_pixel(x: int, y: int) -> Color | None:
    """Get the RGB color of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the canvas.
    """
    if _coordinates_in_bounds(x, y, _settings["width"], _settings["height"]):
        return _screen.get(*_canvas_to_screen(x, y, _settings["left_margin"], _settings["top_margin"]))
    else:
        return None


def set_pixel(x: int, y: int, color: Color = _BLACK) -> None:
    """Set the RGB color of the pixel at the given position (from top left)

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255.
    """
    if _coordinates_in_bounds(x, y, _settings["width"], _settings["height"]):
        # speeds up the function in case color is black
        if color == _BLACK:
            final_color = "black"
        else:
            final_color = _color_tuple_to_hex(color)

        _screen.put(
            final_color,
            to=_canvas_to_screen(x, y, _settings["left_margin"], _settings["top_margin"])
        )


def draw_string(
        x: int,
        y: int,
        text: str,
        color: Color = _BLACK,
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
        if not _coordinates_in_bounds(x, y, _settings["width"], _settings["height"]):
            return

        char_map = _get_char(char, size)
        draw_char()
        x += len(char_map[0])


# functions used only by the package

def _screen_dimensions() -> tuple[int, int]:
    """Calculates the dimensions of the screen"""
    return (
        _settings["left_margin"] + _settings["width"] + _settings["right_margin"],
        _settings["top_margin"] + _settings["height"] + _settings["bottom_margin"]
    )


# window

_window = tk.Tk()
if _settings["show_screen"] is True:
    _window.geometry("{}x{}".format(*_screen_dimensions()))

    _window.grab_release()
    _window.title("casioplot")
    _window.attributes("-topmost", True)
else:
    _window.withdraw()

# screen

if _settings["bg_image_is_set"] is True:
    _screen = tk.PhotoImage(file=_settings["background_image"], )
else:
    width, height = _screen_dimensions()
    _screen = tk.PhotoImage(width=width, height=height)

_screen_display = tk.Label(master=_window, image=_screen, border=0)
_screen_display.pack()
