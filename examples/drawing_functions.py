from math import *
from casioplot import *


def get_color(rgb, rgba):
    r = (rgb[0] * (255 - rgba[3]) + rgba[0] * rgba[3]) / 255
    g = (rgb[1] * (255 - rgba[3]) + rgba[1] * rgba[3]) / 255
    b = (rgb[2] * (255 - rgba[3]) + rgba[2] * rgba[3]) / 255
    return int(r), int(g), int(b)


def draw(p, color=(0, 0, 0)):
    x, y = p
    x += casioplot_settings.get('width') // 2
    y += casioplot_settings.get('height') // 2

    if casioplot_settings.get('width') >= x >= 0 and casioplot_settings.get('height') >= y >= 0:
        bg = get_pixel(x, y)
        if len(color) == 4:
            c = get_color(bg, (color[0], color[1], color[2], color[3]))
        else:
            c = get_color(bg, (color[0], color[1], color[2], 255))

        set_pixel(round(x), round(y), c)
    else:
        print("Warning: Pixel at position ({};{}) doesn't exist.".format(
            x - casioplot_settings.get('width') // 2,
            y - casioplot_settings.get('height') // 2))


def line(p1, p2, color):
    """
    Test of a line drawing function that use trigonometry to find the nearest pixel for each point of a line.
    """
    xa, ya = p1
    xb, yb = p2
    x, y = xa - xb, ya - yb
    d = dist(x, y)
    if x != 0:
        a = atan2(y, x)
        # if x < 0:
        #     a += pi
    elif y > 0:
        a = pi / 2
    else:
        a = 3 * pi / 2
    for i in range(round(d)):
        x1 = round(cos(a) * i) - xa
        y1 = round(sin(a) * i) - ya
        draw((x1, y1), color)


def _f_part(x):
    return x - int(x)


def _reverse_f_part(x):
    return 1 - _f_part(x)


def put_pixel(p, color, alpha=1):
    """
    Paints color over the background at the point xy in img.
    Use alpha for blending. alpha=1 means a completely opaque foreground.
    """

    x, y = p

    bg = get_pixel(x, y)
    if bg is None:
        bg = (255, 255, 255)
    c = get_color(bg, (color[0], color[1], color[2], alpha * 255))
    set_pixel(x, y, c)


def draw_line(p1, p2, color):
    """Draws an anti-aliased line in img from p1 to p2 with the given color."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    steep = abs(dx) < abs(dy)

    def p(px, py):
        return ((px, py), (py, px))[steep]

    if steep:
        x1, y1, x2, y2, dx, dy = y1, x1, y2, x2, dy, dx
    if x2 < x1:
        x1, x2, y1, y2 = x2, x1, y2, y1

    try:
        grad = dy / dx
    except ZeroDivisionError:
        grad = 0
    inter_y = y1 + _reverse_f_part(x1) * grad

    def draw_endpoint(pt):
        x0, y0 = pt
        x0_end = round(x0)
        y_end = y0 + grad * (x0_end - x0)
        x_gap = _reverse_f_part(x0 + 0.5)
        px, py = int(x0_end), int(y_end)
        put_pixel(p(px, py), color, _reverse_f_part(y_end) * x_gap)
        put_pixel(p(px, py + 1), color, _f_part(y_end) * x_gap)
        return px

    x_start = draw_endpoint(p(*p1)) + 1
    x_end = draw_endpoint(p(*p2))

    if x_start > x_end:
        x_start, x_end = x_end, x_start

    for x in range(x_start, x_end):
        y = int(inter_y)
        put_pixel(p(x, y), color, _reverse_f_part(inter_y))
        put_pixel(p(x, y + 1), color, _f_part(inter_y))
        inter_y += grad
