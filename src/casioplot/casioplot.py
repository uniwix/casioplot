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
        _settings["left"] + _settings["width"] + _settings["right"],
        _settings["top"] + _settings["height"] + _settings["bottom"]
    )


def _save_screen(image_suffix: str = "") -> None:
    """Saves the virtual screen as an image

    Only used by the function :py:func:`show_screen`

    :param image_suffix: The setting ``save_multiple`` is True needs to
                         create images with the name :file:`casioplot2.png` for example
    """

    canvas_image: Image.Image = ImageTk.getimage(_canvas)
    background_image: Image.Image = ImageTk.getimage(_background)

    background_image.paste(canvas_image, (_settings["left"], _settings["top"]))

    background_image.save(
        _settings["image_name"] + image_suffix + '.' + _settings["image_format"],
        format=_settings["image_format"],
    )


def _debuging_coordinates(x: int, y: int, function: str) -> None:
    """Prints a message telling if the coordinates are out of bounds

    Used by the functions set_pixel, get_pixel or draw_string
    It is only called if the setting ``debuging_messages`` is true

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param function: the function that called this function
    """
    print(f"Debuging message: you used {function} with coordinates out of bounds")
    if x < 0:
        print(f"    - x must be greater or equal to 0, x = {x}")
    elif x >= _settings["width"]:
        print(f"    - x must be smaller than width, x = {x} and width = {_settings["width"]}")
    if y < 0:
        print(f"    - y must be greater or equal to 0, y = {x}")
    elif y >= _settings["height"]:
        print(f"    - y must be smaller than height, y = {y} and height = {_settings["height"]}")


def _debuging_color(color: Color, function: str) -> None:
    """Prints a message telling if the color is valid

    Used by the functions set_pixel or draw_string
    It is only called if the setting ``debuging_messages`` is true

    :param color: The color of a pixel
    :param function: the function that called this function
    """
    # checks if the color is right
    if 0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255:
        return

    print(f"Debuging message: you used {function} with an invalid color:")
    if color[0] < 0:
        print(f"    - the red channel must be greater or equal to 0, red = {color[0]}")
    elif color[0] > 255:
        print(f"    - the red channel must be smaller or equal to 255, red = {color[0]}")
    if color[1] < 0:
        print(f"    - the green channel must be greater or equal to 0, green = {color[1]}")
    elif color[1] > 255:
        print(f"    - the green channel must be smaller or equal to 255, green = {color[1]}")
    if color[2] < 0:
        print(f"    - the blue channel must be greater or equal to 0, blue = {color[2]}")
    elif color[2] > 255:
        print(f"    - the blue channel must be smaller or equal to 255, blue = {color[2]}")


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
        if _settings["debuging_messages"]:
            _debuging_coordinates(x, y, "get_pixel")
        return None


def set_pixel(x: int, y: int, color: Color = _BLACK) -> None:
    """Set the RGB color of the pixel at the given coordinates

    Using a try statement is faster than checking if the coordinates are in bounds.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The color of a pixel
    """
    if _settings["debuging_messages"]:
        _debuging_color(color, "set_pixel")

    try:
        if _settings["correct_colors"] is True:  # corrects the colors to match the behavior of the casio calculators
            color = (  # there may be a faster way
                color[0] - color[0] % 8,
                color[1] - color[1] % 4,
                color[2] - color[2] % 8
            )

        _canvas.put(
            "#%02x%02x%02x" % color,  # convert the color (RGB tuple) to a hexadecimal string '#RRGGBB'
            to=(x, y)
        )
    except tk.TclError:  # the pixel is out of the canvas
        if _settings["debuging_messages"]:
            _debuging_coordinates(x, y, "set_pixel")



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
    :param color: The color of a pixel
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


    if _settings["debuging_messages"]:
        _debuging_color(color, "draw_string")

    if y < 0 or y >= _settings["height"]:  # checks if the y coordinate is in bounds of the canvas
        if _settings["debuging_messages"]:
            _debuging_coordinates(x, y, "draw_string")
        return

    for char in text:
        if x < 0 or x >= _settings["width"]:  # if the x coordinates isn't in bounds stop
            if _settings["debuging_messages"]:
                _debuging_coordinates(x, y, "draw_string")
            return

        char_map = _get_char(char, size)
        _draw_char()
        x += len(char_map[0])



try:
    # window

    _window = tk.Tk()
    """The tkinter window that shows the virtual screen

    :meta hide-value:
    """

    if _settings["show_screen"] is True:
        _window.geometry("{}x{}".format(*_screen_dimensions()))
        _window.title("casioplot")
        _window.grab_release()
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

    if _settings["bg_in_use"] is True:
        _background = tk.PhotoImage(file=_settings["background"])
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
    _canvas_display = tk.Label(master=_window, image=_canvas, border=0)
    """The tkinter label that shows the canvas

    :meta hide-value:
    """
    _background_display.place(x=0, y=0)
    _canvas_display.place(x=_settings["left"], y=_settings["top"])

except tk.TclError:
    print("The tkinter window couldn't be created. The screen won't be shown.")


@atexit.register
def _run_at_exit() -> None:
    """This function should be called at the end of the program to close the tkinter window"""
    if _settings["save_screen"] is True:  # saves the thes screen as it was before the program ended
        _save_screen()

    if _settings["show_screen"] is True and _settings["close_window"] is False:  # keeps the tkinter window open after the program ends
        _window.mainloop()
