"""This module contains utility functions for the casioplot package"""
import tkinter as tk

from casioplot.settings import _settings


# TODO: Takes too much time so needs improvements
def _coordinates_in_bounds(x: int, y: int) -> bool:
    """Checks if the given coordinates are in bounds of the canvas

    :param x: x coordinate (from the left to the right)
    :param y: y coordinate (from the top to the bottom)
    :return: a bool that says if the given coordinates are in bounds of the canvas
    """
    return 0 <= x < _settings["width"] and 0 <= y < _settings["height"]


def _save_screen(screen: tk.PhotoImage, image_suffix: str = ""):
    """Saves _screen as an image_suffix

    Only used by the function show_screen
    :param image_suffix: If the setting save_multiple is True existes a need to
    create images with the name `casioplot2.png` for example.
    """
    screen.write(
        _settings["filename"] + image_suffix + '.' + _settings["image_format"],
        format=_settings["image_format"],
    )
