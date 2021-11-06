from typing import Literal

from PIL import Image, ImageDraw


_WHITE: tuple[int, int, int] = (255, 255, 255)  # RGBA white

# Create virtual screen
_image: Image.Image = Image.new('RGB', (384, 192), _WHITE)
# Create drawing object (used by the function draw_string
_draw: ImageDraw.ImageDraw = ImageDraw.Draw(_image)


class Settings:
    width: int = 384  # Screen width in pixels
    height: int = 192  # Screen height in pixels
    filename: str = "casioplot.png"
    image_format: str = "png"
    left_margin: int = 0
    right_margin: int = 0
    top_margin: int = 0
    bottom_margin: int = 0

    def _clear_screen(self):
        global _image, _draw
        _image = Image.new('RGB', (
            self.left_margin + self.width + self.right_margin,
            self.top_margin + self.height + self.bottom_margin
        ), _WHITE)  # Create a new white image
        _draw = ImageDraw.Draw(_image)

    def default(self):
        for k, v in Settings.__dict__:
            self.__setattr__(k, v)
        self._clear_screen()

    def casio_graph_90_plus_e(self):
        """
        Set the screen in the casio Graph 90+e format
        """
        global _image, _draw
        self.width = 384
        self.height = 192
        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 24
        self.bottom_margin = 0

        _image = Image.open('CASIO_Graph_90+e_empty.png').convert("RGB")
        for x in range(self.width):
            for y in range(self.height):
                _image.putpixel((x + self.left_margin, y + self.top_margin), _WHITE)
        _draw = ImageDraw.Draw(_image)

    def set(self, key: str, value):
        self.__setattr__(key, value)
        self._clear_screen()


casioplot_settings = Settings()


def show_screen():
    """
    Show the virtual screen.
    Save the screen as casio.png.
    """
    # image.show() # open the picture
    _image.save(casioplot_settings.filename, format=casioplot_settings.image_format)  # save the screen to the disk
    # as "casio.png"


def clear_screen():
    """
    Clear the virtual screen.
    """
    show_screen()
    casioplot_settings.default()


def get_pixel(x: int, y: int) -> tuple[int, int, int] | None:
    """
    Get the color RGB of the pixel at the given position.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :return: The pixel color. A tuple that contain 3 integers from 0 to 255 or None if the pixel is out of the screen.
    """
    if not 0 <= x <= casioplot_settings.width or not 0 <= y <= casioplot_settings.height:
        return None
    r: int
    g: int
    b: int
    r, g, b = _image.getpixel((x + casioplot_settings.left_margin, y + casioplot_settings.top_margin))
    return r, g, b


def set_pixel(x: int, y: int, color: tuple[int, int, int] = (0, 0, 0)):
    """
    Set the color RGB of the pixel at the given position (from top left)

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param color: The pixel color. A tuple that contain 3 integers from 0 to 255.
    """
    if not 0 <= x <= casioplot_settings.width or not 0 <= y <= casioplot_settings.height:
        return
    _image.putpixel((x + casioplot_settings.left_margin, y + casioplot_settings.top_margin), color)


def draw_string(x: int,
                y: int,
                text: str,
                color: tuple[int, int, int] = (0, 0, 0),
                size: Literal["small", "medium", "large"] = "medium"):
    """
    Draw a string on the virtual screen with the given color RGB.

    :param x: x coordinate (from the left)
    :param y: y coordinate (from the top)
    :param text: text that will be shown
    :param color: The text color. A tuple that contain 3 integers from 0 to 255.
    :param size: Size of the text. String from the following values: "small", "medium" or "large".
                 This parameter isn't implemented yet.
    """
    # The size and the font used by casio are unknown so they aren't implemented.
    print('Warning: Size and font are not implemented yet.')
    print('         Default font and size will be used.')
    # Write the text on the virtual screen.
    _draw.text((x + casioplot_settings.left_margin, y + casioplot_settings.top_margin), text, fill=color)
