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
from PIL import Image, ImageTk

from casioplot.characters import _get_char
from casioplot.settings import _settings
from casioplot.types import Color

# some frequently used colors
_WHITE: Color = (255, 255, 255)  # RGB white
_BLACK: Color = (0, 0, 0)  # RGBA black

# these two are only used if the setting save_multiple is set to True
save_screen_counter = 0
current_image_number = 1


# functions used by the package


def _screen_dimensions() -> tuple[int, int]:
    """Calculates the dimensions of the screen"""
    return (
        _settings["left_margin"] + _settings["width"] + _settings["right_margin"],
        _settings["top_margin"] + _settings["height"] + _settings["bottom_margin"]
    )


def _save_screen(image_suffix: str = ""):
    """Saves _screen as an image_suffix

    Only used by the function show_screen
    :param image_suffix: If the setting save_multiple is True existes a need to
    create images with the name `casioplot2.png` for example.
    """

    if settings["bg_image_is_set"] is True:
        canvas_image: Image.Image = ImageTk.getimage(_canvas)
        background_image: Image.Image = ImageTk.getimage(_background)

        background_image.paste(canvas_image, (settings["left_margin"], settings["top_margin"]))

        background_image.save(
            _settings["image_name"] + image_suffix + '.' + _settings["image_format"],
            format=_settings["image_format"],
        )
    else:
        # the approach used above would save the screen properly, but this is faster
        _canvas.write(
            _settings["image_name"] + image_suffix + '.' + _settings["image_format"],
            format=_settings["image_format"],
        )


# functions for the user


def show_screen() -> None:
    """Show or saves the virtual screen

    This function implement two modes that can be enabled or disabled using the :py:class:`casioplot_settings`:
      - show the screen as an image, if `show_screen` is True
      - Save the screen to the disk, if `save_screen` in True
        The image is saved with the image_name found in `image_name`
    """

    if _settings["show_screen"] is True:
        # show the screen
        _window.update()

    if _settings["save_screen"] is True:
        if _settings["save_multiple"] is True:
            global save_screen_counter, current_image_number
            if save_screen_counter == _settings["save_rate"]:
                _save_screen(str(current_image_number))
                current_image_number += 1
                save_screen_counter = 0

            save_screen_counter += 1
        else:
            # When the program ends, the saved image will show the screen as it was in the last call of show_screen
            _save_screen()


def clear_screen() -> None:
    """Clear the virtual screen"""
    _canvas.put(
        "white",
        to=(0, 0, _settings["width"], _settings["height"])
    )


def get_pixel(x: int, y: int) -> Color | None:
    """Get the RGB color of the pixel at the given position.

    Using a try statment is faster than checking if the coordinates are in bounds.
    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the canvas
    """
    try:
        return _canvas.get(x, y)
    except tk.TclError:
        return None


def set_pixel(x: int, y: int, color: Color = _BLACK) -> None:
    """Set the RGB color of the pixel at the given position (from top left)

    Using a try statement is faster than checking if the coordinates are in bounds.
    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255
    """
    try:
        _canvas.put(
            "#%02x%02x%02x" % color,  # convert the color (RGB tuple) to a hexadecimal string '#RRGGBB'
            to=(x, y)
        )
    except tk.TclError:
        # the pixel is out of the canvas
        pass


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
    :param color: The color of the text. A tuple that contain 3 integers from 0 to 255
    :param size: Size of the text. String from the following values: "small", "medium" or "large"
    :raise ValueError: Raise a ValueError if the size isn't correct
    """

    def draw_char() -> None:
        """Draws a single character"""
        for y2, row in enumerate(char_map):
            for x2, pixel in enumerate(row):
                if pixel == 'X':
                    set_pixel(x + x2, y + y2, color)

    for char in text:
        if not (0 <= x < _settings["width"] and 0 <= y < _settings["height"]):  # if coordinates aren't in bounds stop
            return

        char_map = _get_char(char, size)
        draw_char()
        x += len(char_map[0])



# window

_window = tk.Tk()
if _settings["show_screen"] is True:
    _window.geometry("{}x{}".format(*_screen_dimensions()))

    _window.grab_release()
    _window.title("casioplot")
    _window.attributes("-topmost", True)
    _window.resizable(False, False)
else:
    _window.withdraw()

# screen

_canvas = tk.PhotoImage(width=_settings["width"], height=_settings["height"])
clear_screen()  # ensures the pixels are set to white and not transparent

if _settings["bg_image_is_set"] is True:
    _background = tk.PhotoImage(file=_settings["background_image"])
else:
    bg_width, bg_height = _screen_dimensions()
    _background = tk.PhotoImage(width=bg_width, height=bg_height)
    _background.put(  # same as clear_screen but for the background image
        "white",
        to=(0, 0, bg_width, bg_height)
    )

_background_display = tk.Label(master=_window, image=_background, border=0)
_background_display.place(x=0, y=0)
_canvas_display = tk.Label(master=_window, image=_canvas, border=0)
_canvas_display.place(x=_settings["left_margin"], y=_settings["top_margin"])

