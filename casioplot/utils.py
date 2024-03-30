"""This module contains utility functions for the casioplot package"""
import tkinter as tk

from casioplot.types import Color


def _canvas_to_screen(x: int, y: int, start_x: int, start_y: int) -> tuple[int, int]:
    """Converts coordinates to canvas coordinates

    :param x: x coordinate (from the left to the right)
    :param y: y coordinate (from the top to the bottom)
    :param start_x: the x coordinate of the top left corner of the canvas
    :param start_y: the y coordinate of the top left corner of the canvas
    :return: a tuple with the canvas coordinates
    """
    return x + start_x, y + start_y


# TODO: Takes too much time so needs improvements
def _coordinates_in_bounds(x: int, y: int, max_x: int, max_y: int) -> bool:
    """Checks if the given coordinates are in bounds of the canvas

    :param x: x coordinate (from the left to the right)
    :param y: y coordinate (from the top to the bottom)
    :param max_x: the maximum x coordinate
    :param max_y: the maximum y coordinate
    :return: a bool that says if the given coordinates are in bounds of the canvas
    """
    return 0 <= x < max_x and 0 <= y < max_y


def _save_screen(screen: tk.PhotoImage, filename: str, image_format: str, image_suffix: str = ""):
    """Saves _screen as an image_suffix

    Only used by the function show_screen
    :param image_suffix: If the setting save_multiple is True existes a need to
    create images with the name `casioplot2.png` for example.
    """
    screen.write(
        filename + image_suffix + '.' + image_format,
        format=image_format,
    )


def _color_tuple_to_hex(color: Color) -> str:
    """Converts a color tuple to a string

    :param color: a color tuple
    :return: a string that represents the color
    """
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
