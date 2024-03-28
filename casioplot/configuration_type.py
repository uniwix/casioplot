"""This file contains the type `configuration`

This type makes it possible to representing all settings and configs in a dictionary but still
have type annotations for every settings.
"""

from typing import TypedDict

from PIL import Image


# the option `total=False` makes it possible for a configuration
# to not have a corresponding value for all settings
class configuration(TypedDict, total=False):
    # canvas size
    width: int  # canvas width in pixels
    height: int  # canvas height in pixels

    # margins
    left_margin: int
    right_margin: int
    top_margin: int
    bottom_margin: int

    # background Image
    bg_image_is_set: bool  # is used when changing settings, if it is False the background_image
    # will be ignored
    background_image: Image.Image  # some configs like casio_graph_90_plus_e
    # have a special background image
    #
    # Output settings
    show_screen: bool  # Show the screen, do not mistake for the function show_screen()
    save_screen: bool  # Save the screen as an image

    # Saving settings
    filename: str
    image_format: str
    save_multiple: bool  # save multiple images so that the user can examine better the screen
    save_rate: int  # if save_multiple is True a new image will be saved
    # every `save_rate` times show_screen is called
