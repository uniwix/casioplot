from typing import TypedDict
from PIL import Image


class configuration(TypedDict):
    # canvas size
    width: int  # canvas width in pixels
    height: int  # canvas height in pixels
    # margins
    left_margin: int
    right_margin: int
    top_margin: int
    bottom_margin: int
    # background Image
    bg_image_is_set: bool  # is used when changing settings
    background_image: Image.Image  # some configs like casio_graph_90_plus_e
    # have a special background image
    # Output settings
    show_screen: bool  # Show the screen, do not misstake for the functin show_screen()
    save_screen: bool  # Save the screen as an image
    # Saving settings
    filename: str
    image_format: str
