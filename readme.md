# Casioplot for computer

Module *casioplot* from Casio calculator for Computer.

This can help to develop python programs in your computer and run it before put it in your calculator.

## Requirements

This module use python 3.10.0.

Need the module *Pillow* to work.

### Install *Pillow*:

```bash
$ pip install pillow
```

## Settings

See [settings options](settings.md) for more information.

## Exemples

### Draw a pixel

```python
from casioplot import *

red = (255, 0, 0)
set_pixel(10, 10, red)
show_screen()  # Don't forget to show the screen to see the result.
```

#### Result:

![pixel](images/pixel.png)

### Draw a rectangle

```python
from casioplot import *


def rectangle(start_x, start_y, end_x, end_y, color):
    x = abs(end_x - start_x)
    y = abs(end_y - start_y)
    for i in range(x + 1):
        for j in range(y + 1):
            set_pixel(i + start_x, j + start_y, color)


red = (255, 0, 0)
rectangle(10, 10, 200, 100, red)
show_screen()  # Don't forget to show the screen to see the result.
```

#### Result:

![rectangle](images/rectangle.png)

### Get a pixel value

```python
from casioplot import *


def rectangle(start_x, start_y, end_x, end_y, color):
    x = abs(end_x - start_x)
    y = abs(end_y - start_y)
    for i in range(x + 1):
        for j in range(y + 1):
            set_pixel(i + start_x, j + start_y, color)


red = (255, 0, 0)
rectangle(10, 10, 200, 100, red)

match get_pixel(20, 20):
    case r, g, b:
        print('Red:  ', r)
        print('Green:', g)
        print('Blue: ', b)
    case None:
        print('Out of the screen.')

```

#### Result:

```
Red:   255
Green: 0
Blue:  0
```

Note that you don't need to show the screen to get the color of a pixel.

## Compatibility Notes

Some behaviors aren't respected:

- The output isn't show in the screen but saved on a picture.
- The function **draw_string** ignore the *size* parameter and doesn't use the same font as casio.
- Only one calculator implemented: **casio graph 90+e**

---------------------------
v 1.0.0 - Uniwix
