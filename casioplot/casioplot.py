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
from casioplot.settings import _get_settings
from casioplot.types import Configuration, Color
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

    if settings["show_screen"] is True:
        # show the screen
        global screen
        new_screen = virtual_screen.copy()
        label_screen.configure(image=new_screen)
        screen = new_screen
        window.update()

    if settings["save_screen"] is True:
        if settings["save_multiple"] is True:
            global save_screen_counter, current_image_number
            if save_screen_counter == settings["save_rate"]:
                _save_screen(screen, settings["filename"], settings["image_format"], str(current_image_number))
                current_image_number += 1
                save_screen_counter = 0

            save_screen_counter += 1
        else:
            # When the program ends, the saved image will show the screen as it was in the last call of show_screen
            _save_screen(screen, settings["filename"], settings["image_format"])


def clear_screen() -> None:
    """Clear the virtual screen"""
    virtual_screen.put(
        "white",
        (
            settings["left_margin"],
            settings["top_margin"],
            settings["left_margin"] + settings["width"],
            settings["top_margin"] + settings["height"]
        )
    )


def get_pixel(x: int, y: int) -> Color | None:
    """Get the RGB color of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the canvas.
    """
    if _coordinates_in_bounds(x, y, settings["width"], settings["height"]):
        return virtual_screen.get(*_canvas_to_screen(x, y, settings["left_margin"], settings["top_margin"]))
    else:
        return None


def set_pixel(x: int, y: int, color: Color = _BLACK) -> None:
    """Set the RGB color of the pixel at the given position (from top left)

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255.
    """
    if _coordinates_in_bounds(x, y, settings["width"], settings["height"]):
        virtual_screen.put(
            _color_tuple_to_hex(color),
            _canvas_to_screen(x, y, settings["left_margin"], settings["top_margin"])
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
        if not _coordinates_in_bounds(x, y, settings["width"], settings["height"]):
            return

        char_map = _get_char(char, size)
        draw_char()
        x += len(char_map[0])


# functions used only by the package

def _screen_dimensions() -> tuple[int, int]:
    """Calculates the dimensions of the screen"""
    return (
        settings["left_margin"] + settings["width"] + settings["right_margin"],
        settings["top_margin"] + settings["height"] + settings["bottom_margin"]
    )


settings: Configuration = _get_settings()

if settings["show_screen"] is True:
    # Creates a tkinter window
    window = tk.Tk()
    width, height = _screen_dimensions()
    window.geometry(f"{width}x{height}")

    window.grab_release()
    window.title("casioplot")
    window.attributes("-topmost", True)
else:
    window = None

# Create images

if settings["bg_image_is_set"] is True:
    screen = tk.PhotoImage(
        master=window,
        file=settings["background_image"],
    )
    virtual_screen = screen.copy()

    bg_width, bg_height = screen.width(), screen.height()

    settings["width"] = bg_width - (settings["left_margin"] + settings["right_margin"])
    settings["height"] = bg_height - (settings["top_margin"] + settings["bottom_margin"])

    width, height = _screen_dimensions()
    window.geometry(f"{width}x{height}")

else:
    width, height = _screen_dimensions()
    window.geometry(f"{width}x{height}")
    screen = tk.PhotoImage(master=window, width=width, height=height)
    virtual_screen = tk.PhotoImage(master=window, width=width, height=height)

if settings["show_screen"] is True:
    label_screen = tk.Label(master=window, image=screen, border=0)
    label_screen.pack()
