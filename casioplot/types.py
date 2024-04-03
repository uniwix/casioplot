"""This file contains the type :py:class:`Configuration` and the type :py:class:`Color`.

The type :py:class:`Configuration` makes it possible to representing all settings and configs in a dictionary but still
have type annotations for every setting.
"""

from typing import TypedDict


# the option :python:`total=False` makes it possible for a configuration
# to not have a value for all settings
class Configuration(TypedDict, total=False):
    # canvas size
    width: int  # canvas width in pixels
    height: int  # canvas height in pixels

    # margins
    left_margin: int
    right_margin: int
    top_margin: int
    bottom_margin: int

    # background
    bg_image_is_set: bool  # if it is False the background_image will be ignored
    background_image: str  # some config files like `graph_90+e.toml`
    # have a special background image

    # showing_screen
    show_screen: bool  # do not mistake for the function `show_screen` from `casioplot.py`

    # saving_screen
    save_screen: bool  # Save the screen as an image
    image_name: str
    image_format: str  # should be one of the following image formats: jpeg, jpg, png, gif, bmp, tiff or tif
    save_multiple: bool  # save multiple images so that the user can examine better the virtual screen
    save_rate: int  # if `save_multiple is True a new image will be saved`
    # every `save_rate` times show_screen is called


Color = tuple[int, int, int]
"""A color is represented as a tuple of three integers, each integer is in the range [0, 255] and represents the
intensity of the color in the red, green and blue channels respectively."""
