import tkinter as tk

from casioplot.configuration_type import configuration
from casioplot.get_config import _get_settings

# TODO: use settings instead of hardcoded values
# TODO: implement save screen
# TODO: change how characters are drawn to be more efficient and faster

# get the settings
settings: configuration = _get_settings()


def _screen_dimensions() -> tuple[int, int]:
    """Calculates the dimensions of the screen"""
    return (
        settings["left_margin"] + settings["width"] + settings["right_margin"],
        settings["top_margin"] + settings["height"] + settings["bottom_margin"]
    )


# Create the window
window = tk.Tk()
width, height = _screen_dimensions()
window.geometry(f"{width}x{height}")
window.title("casioplot")
window.attributes("-topmost", True)
window.deiconify()

# Create images
# TODO: change settings to store the path to the background image instead of the image itself
background_image = tk.PhotoImage(master=window,
                                 file='/mnt/147CDBD07CDBAAAE/Users/jbeno/PycharmProjects/casioplot/casioplot/images/calculator.png')
screen = tk.PhotoImage(master=window, width=settings["width"], height=settings["height"])
virtual_screen = tk.PhotoImage(master=window, width=settings["width"], height=settings["height"])

# Create labels (that hold the images)
label_bg = tk.Label(master=window, image=background_image, border=0)
label_bg.pack()
label_bg.place(relx=0.0, rely=0.0, x=0, y=0, anchor="nw")
label_screen = tk.Label(master=window, image=screen, border=0)
label_screen.pack()
label_screen.place(relx=0.0, rely=0.0, x=settings["left_margin"], y=settings["top_margin"], anchor="nw")


def set_pixel(x: int, y: int, color=(0, 0, 0)):
    try:
        virtual_screen.put(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}", (x, y))
    except tk.TclError:  # if the pixel is out of bounds
        return None


def get_pixel(x: int, y: int):
    try:
        return virtual_screen.get(x, y)
    except tk.TclError:  # if the pixel is out of bounds
        return None


def clear_screen():
    virtual_screen.put("#ffffff", (0, 0, settings["width"], settings["height"]))


def show_screen():
    # new_screen is for updating canvas before deleting the old image
    global screen
    new_screen = virtual_screen.copy()
    label_screen.configure(image=new_screen)
    screen = new_screen
    window.update()
