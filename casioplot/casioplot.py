"""Contains all the functions from ``casioplot`` calculator module.

Available functions:
  - :py:func:`set_pixel`
  - :py:func:`get_pixel`
  - :py:func:`draw_string`
  - :py:func:`clear_screen`
  - :py:func:`show_screen`

You can also use :py:data:`casioplot_settings` to change some behavior.
"""

import os

from typing import Literal

from PIL import Image, ImageDraw

_WHITE: tuple[int, int, int] = (255, 255, 255)  # RGBA white

# Create virtual screen
_image: Image.Image = Image.new('RGB', (384, 192), _WHITE)
# Create drawing object (used by the function draw_string
_draw: ImageDraw.ImageDraw = ImageDraw.Draw(_image)


class casioplot_settings:
    """Manage settings for the casioplot module."""
    
    class Settings:
        """Store default settings"""
        # Size settings
        width: int = 384  # Screen width in pixels
        height: int = 192  # Screen height in pixels
        
        left_margin: int = 0
        right_margin: int = 0
        top_margin: int = 0
        bottom_margin: int = 0
        
        # Output settings
        open_image: bool = False  # Open the screen
        save_image: bool = True  # Save the screen as an image
        # Saving settings
        filename: str = "casioplot.png"
        image_format: str = "png"
    
    @classmethod
    def _clear_screen(cls):
        """Clear the screen.
        
        It creates a new image and assigns it to global _image.
        """
        global _image, _draw
        
        _image = Image.new('RGB', (
            cls.left_margin + cls.width + cls.right_margin,
            cls.top_margin + cls.height + cls.bottom_margin
        ), _WHITE)  # Create a new white image
        
        _draw = ImageDraw.Draw(_image)
    
    @classmethod
    def default(cls):
        """Restore default parameters from the class to the instance."""
        for k, v in casioplot_settings.Settings.__dict__.items():
            setattr(cls, k, v)
        cls._clear_screen()
    
    @classmethod
    def casio_graph_90_plus_e(cls):
        """Set the screen in the casio Graph 90+e format."""
        global _image, _draw
        cls.width = 384
        cls.height = 192
        cls.left_margin = 0
        cls.right_margin = 0
        cls.top_margin = 24
        cls.bottom_margin = 0
        
        # Get the path of the template image
        import os

        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'images',
                                 'CASIO_Graph_90+e_empty.png')
        _image = Image.open(file_path).convert("RGB")
        _draw = ImageDraw.Draw(_image)
    
    @classmethod
    def set(cls, **settings):
        """Set an attribute for each given setting with the corresponding value.
        """
        for setting, value in settings.items():
            setattr(cls, setting, value)
        cls._clear_screen()
    
    @classmethod
    def get(cls, setting):
        return cls.__dict__.get(setting, cls.Settings.__dict__.get(setting))


def show_screen():
    """Show the virtual screen
    
    This function implement two modes that can be enabled or disabled using the :py:class:`casioplot_settings`:
      - Open the screen as an image (enabled using `casioplot_settings.get('open_image')`).
      - Save the screen to the disk (enabled using `casioplot_settings.get('save_image')`).
        The image is saved with the filename found in `casioplot_settings.get('filename')`
    """
    if casioplot_settings.get('open_image'):
        # open the picture
        _image.show()
    if casioplot_settings.get('save_image'):
        # Save the screen to the disk as an image with the given filename
        _image.save(casioplot_settings.get('filename'), format=casioplot_settings.get('image_format'))


def clear_screen():
    """Clear the virtual screen."""
    show_screen()
    casioplot_settings.default()


def get_pixel(x: int, y: int) -> tuple[int, int, int] | None:
    """Get the RGB color of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the screen.
    """
    if not 0 <= x <= casioplot_settings.get('width') - 1 or not 0 <= y <= casioplot_settings.get('height') - 1:
        return None
    r: int
    g: int
    b: int
    r, g, b = _image.getpixel((x + casioplot_settings.get('left_margin'), y + casioplot_settings.get('top_margin')))
    return r, g, b


def set_pixel(x: int, y: int, color: tuple[int, int, int] = (0, 0, 0)):
    """Set the RGB color of the pixel at the given position (from top left)

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255.
    """
    if not 0 <= x < casioplot_settings.get('width') - 1 or not 0 <= y < casioplot_settings.get('height') - 1:
        return
    _image.putpixel((x + casioplot_settings.get('left_margin'), y + casioplot_settings.get('top_margin')), color)


def _get_filename(character, size: Literal["small", "medium", "large"] = "medium"):
    """Get the file where a character is saved and return the ``space`` file if the character doesn't exist.
    
    :param character: The character to find
    :param size: The size of the character
    :return: The character filename. A string: "{``./chars`` folder absolute path}/{character}_{size}.png"
    """
    special_chars = {
        ' ': 'space'
    }
    filename = special_chars.get(character, character) + '.txt'
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             'chars',
                             size,
                             filename)

    if not os.path.isfile(file_path):
        print(f'WARNING: No character "{character}" found for size "{size}".')
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'chars',
                                 size,
                                 'space.txt')
    return file_path


def draw_string(x: int,
                y: int,
                text: str,
                color: tuple[int, int, int] = (0, 0, 0),
                size: Literal["small", "medium", "large"] = "medium"):
    """Draw a string on the virtual screen with the given RGB color and size.
    
    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param text: text that will be shown
    :param color: The text color. A tuple that contain 3 integers from 0 to 255.
    :param size: Size of the text. String from the following values: "small", "medium" or "large".
    :raise ValueError: Raise a ValueError if the size isn't correct.
    """
    sizes = {
        'small': (10, 10),
        'medium': (13, 17),
        'large': (18, 23)
    }
    
    if size not in sizes.keys():
        raise ValueError(f'Unknown size "{size}". Size must be one of the following: "small", "medium" or "large"')
    
    for character in text:
        filename = _get_filename(character, size)
        n = 0
        with open(filename, 'r') as c:
            count = 0
            for line in c:
                for j, k in enumerate(line):
                    if k in ["$"]:
                        set_pixel(x+j, y+count, color)
                    n = j
                count += 1
        x += n
