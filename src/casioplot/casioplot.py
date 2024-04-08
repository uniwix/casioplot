"""Contains all the functions from :py:mod:`casioplot` calculator module.

Available functions for the user:
  - :py:func:`show_screen`
  - :py:func:`clear_screen`
  - :py:func:`set_pixel`
  - :py:func:`get_pixel`
  - :py:func:`draw_string`

Contains the original functions from the :py:mod:`casioplot` calculator module
and the code needed to emulate the screen.
"""
import atexit
import tkinter as tk

from PIL import Image, ImageTk  # used to save the screen
from casioplot.characters import _get_char
from casioplot.settings import _settings
from casioplot.types import Color, Text_size

# some frequently used colors
_WHITE: Color = (255, 255, 255)
"""RGB white"""

_BLACK: Color = (0, 0, 0)
"""RGB black"""

# these two are only used if the setting save_multiple is set to True
_save_screen_counter = 1
"""Counter used to save multiple images of the screen"""
_current_image_number = 1
"""The number of the current image that is being saved"""


# functions used by the package


def _screen_dimensions() -> tuple[int, int]:
    """Calculates the dimensions of the screen in pixels"""
    return (
        _settings["left_margin"] + _settings["width"] + _settings["right_margin"],
        _settings["top_margin"] + _settings["height"] + _settings["bottom_margin"]
    )


def _save_screen(image_suffix: str = "") -> None:
    """Saves the virtual screen as an image

    Only used by the function :py:func:`show_screen`

    :param image_suffix: The setting ``save_multiple`` is True needs to
                         create images with the name :file:`casioplot2.png` for example
    """

    canvas_image: Image.Image = ImageTk.getimage(_canvas)
    background_image: Image.Image = ImageTk.getimage(_background)

    background_image.paste(canvas_image, (_settings["left_margin"], _settings["top_margin"]))

    background_image.save(
        _settings["image_name"] + image_suffix + '.' + _settings["image_format"],
        format=_settings["image_format"],
    )


# functions for the user


def show_screen() -> None:
    """Shows or saves the virtual screen

    This function implement two distinct modes:

      - show the virtual screen in real time in a tkinter window, if ``show_screen`` is True
      - Save the virtual screen to the disk, if ``save_screen`` in True

    These modes are independent and can work at the same time
    """

    if _settings["show_screen"] is True:
        # the virtual screen is already updated, the tkinter window just needs to update what it is showing
        _window.update()

    if _settings["save_screen"] is True and _settings["save_multiple"] is True:
        global _save_screen_counter, _current_image_number
        if _save_screen_counter == _settings["save_rate"]:
            _save_screen(str(_current_image_number))
            _current_image_number += 1
            _save_screen_counter = 1
        else:
            _save_screen_counter += 1


def clear_screen() -> None:
    """Clear the canvas, sets every pixel to white"""
    _canvas.put(
        "white",
        to=(0, 0, _settings["width"], _settings["height"])
    )


def get_pixel(x: int, y: int) -> Color | None:
    """Get the RGB color of the pixel at the given coordinates of the canvas

    Using a try statement is faster than checking if the coordinates are in bounds

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the canvas
    """
    try:
        return _canvas.get(x, y)
    except tk.TclError:  # the pixel is out of the canvas
        return None


def set_pixel(x: int, y: int, color: Color = _BLACK) -> None:
    """Set the RGB color of the pixel at the given coordinates

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
    except tk.TclError:  # the pixel is out of the canvas
        pass


def draw_string(
        x: int,
        y: int,
        text: str,
        color: Color = _BLACK,
        size: Text_size = "medium"
) -> None:
    """Draw a string on the canvas with the given RGB color and size.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param text: text that will be drawn
    :param color: The color of the text. A tuple that contain 3 integers from 0 to 255
    :param size: Size of the text.
                 String from the following values: :python:`"small"`, :python:`"medium"` or :python:`"large"`
    :raise ValueError: Raise a :py:exc:`ValueError` if the size isn't correct
    """

    def _draw_char() -> None:
        """Draws a single character"""
        for y2, row in enumerate(char_map):
            for x2, pixel in enumerate(row):
                if pixel == 'X':
                    set_pixel(x + x2, y + y2, color)

    for char in text:
        if not (0 <= x < _settings["width"] and 0 <= y < _settings["height"]):  # if coordinates aren't in bounds stop
            return

        char_map = _get_char(char, size)
        _draw_char()
        x += len(char_map[0])


# window
try:
    _window = tk.Tk()
    """The tkinter window that shows the virtual screen

    :meta hide-value:
    """

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
    """The canvas that the user can interact with using the functions from this module

    :meta hide-value:
    """
    clear_screen()  # ensures the pixels are set to white and not transparent

    if _settings["bg_image_is_set"] is True:
        _background = tk.PhotoImage(file=_settings["background_image"])
        """The background image that is shown behind the canvas

        :meta hide-value:
        """
    else:
        bg_width, bg_height = _screen_dimensions()
        _background = tk.PhotoImage(width=bg_width, height=bg_height)
        _background.put(  # same as clear_screen but for the background image
            "white",
            to=(0, 0, bg_width, bg_height)
        )

    _background_display = tk.Label(master=_window, image=_background, border=0)
    """The tkinter label that shows the background image

    :meta hide-value:
    """
    _background_display.place(x=0, y=0)
    _canvas_display = tk.Label(master=_window, image=_canvas, border=0)
    """The tkinter label that shows the canvas

    :meta hide-value:
    """
    _canvas_display.place(x=_settings["left_margin"], y=_settings["top_margin"])
except tk.TclError:
    print("The tkinter window couldn't be created. The screen won't be shown.")


@atexit.register
def run_at_exit() -> None:
    """This function should be called at the end of the program to close the tkinter window"""
    if _settings["save_screen"] is True:  # saves the thes screen as it was before the program ended
        _save_screen()
    if _settings["show_screen"] is True:  # keeps the tkinter window open after the program ends
        if _settings["close_window"] is True:
            _window.destroy()
        else:
            _window.mainloop()
