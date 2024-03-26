from typing import Literal

small = {
    'a': ()
}

medium = {}

large = {}


def _get_char(char: str, size: Literal["small", "medium", "large"] = "medium") -> tuple:
    """Gets the char_map of a character in a given size

    :param char: The character
    :param size: The size of the character
    """
    if char not in small.keys() and char not in medium.keys() and char not in large.keys():
        raise ValueError(f"character {char} not implemented")

    if size == 'small':
        return small[char]
    elif size == 'medium':
        return medium[char]
    else:
        return large[char]
