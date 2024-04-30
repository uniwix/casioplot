"""This file contains the types :py:class:`Configuration`, :py:class:`Color` and :py:class:`Text_size`"""

from typing import TypedDict, Literal


class Configuration(TypedDict):
    """The type :py:class:`Configuration` makes it possible to representing all settings and configs in a dictionary
    but still have type annotations for every setting."""

    # canvas size
    width: int  # canvas width in pixels
    height: int  # canvas height in pixels

    # margins
    left: int
    right: int
    top: int
    bottom: int

    # background
    bg_in_use: bool  # if it is False the background image will be ignored
    background: str  # some config files like `graph_90+e.toml`
    # have a special background image

    # showing_screen
    show_screen: bool  # do not mistake for the function `show_screen` from `casioplot.py
    close_window: bool  # close the window at exit

    # saving_screen
    save_screen: bool  # Save the screen as an image
    image_name: str
    image_format: str  # should be one of the following image formats: jpeg, jpg, png, gif, bmp, tiff or tif
    save_multiple: bool  # save multiple images so that the user can examine better the virtual screen
    save_rate: int  # if `save_multiple is True a new image will be saved`
    # every `save_rate` times show_screen is called

    correct_colors: bool  # the casio calculators don't have the same precission for colors as the computer
    # this options makes the set_pixel function correct the colors to match what would happen in the calculators

    debuging_messages: bool  # activates debuging messages that warn if the program is trying to use get_pixel,
    # set_pixel or draw_string with coordinates outside the canvas

Color = tuple[int, int, int]
"""A color is represented as a tuple of three integers, each integer is in the range [0, 255] and represents the
intensity of the color in the red, green and blue channels respectively."""


Text_size = Literal["small", "medium", "large"]
"""The three accpeted text sizes"""
