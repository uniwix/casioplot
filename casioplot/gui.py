# inspired by https://stackoverflow.com/a/64329015
import threading
import tkinter as tk


# TODO: use settings instead of hardcoded values
# TODO: implement save screen
# TODO: change how characters are drawn to be more efficient and faster
class Screen:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.image = tk.PhotoImage(width=width, height=height)

    def set_pixel(self, x: int, y: int, color=(0, 0, 0)):
        self.image.put(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}", (x, y))

    def get_pixel(self, x: int, y: int):
        return self.image.get(x, y)

    def clear_screen(self):
        self.image.put("#ffffff", (0, 0, self.width, self.height))

    def get_screen(self):
        return self.image.copy()


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("420x248")
        self.title("casioplot")
        self.attributes("-topmost", True)

        self.background_image = tk.PhotoImage(
            file='/mnt/147CDBD07CDBAAAE/Users/jbeno/PycharmProjects/casioplot/casioplot/images/calculator.png')
        self.screen = tk.PhotoImage(width=384, height=192)
        self.virtual_screen = Screen(width=384, height=192)

        # self.label = tk.Label(image=self.image)
        # self.label.pack()
        self.canvas = tk.Canvas(self, width=402, height=230, bg="ivory")
        self.canvas.pack(padx=9, pady=9)
        self.canvas.create_image((201, 115), image=self.background_image)
        self.screen_element = self.canvas.create_image((201, 123), image=self.screen)

    def show_screen(self):
        # new_screen is for updating canvas before deleting the old image
        new_screen = self.virtual_screen.get_screen()
        self.canvas.itemconfig(self.screen_element, image=new_screen)
        self.screen = new_screen

    def clear_screen(self):
        self.virtual_screen.clear_screen()
        self.show_screen()

    def run(self):
        self.mainloop()


class runtk:
    """Instance of the window and the main loop.

    Allows to run the tkinter main loop in a background thread.
    It ensures that the window is running in the same thread as the one it was created in.
    """

    def __call__(self):  # runs in background thread
        self.window = Window()
        self.window.run()


rtk = runtk()
thd = threading.Thread(target=rtk)  # gui thread
thd.daemon = True  # background thread will exit if main thread exits
thd.start()  # start tk loop
