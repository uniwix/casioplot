from time import sleep
import casioplot.casioplot as csp
from casioplot.casioplot import print_test, test
from drawing_functions import *
from casioplot import *

R_2D = pi / 3  # 2D rotation angle (radians)
R_3D = pi / 6  # 3D rotation angle (radians)

casioplot_settings.config_to("casio_graph_90_plus_e")  # Use the casio graph 90+e screen template


def dist(x, y):
    """Get the distance between a point and the origin."""
    return sqrt(x ** 2 + y ** 2)


def rotate_2d(x, y, a):
    """Rotate a point with the given angle (in radians) and the origin."""
    d = dist(x, y)
    b = atan2(y, x) + a
    # if x < 0:
    #     b += pi
    return cos(b) * d, sin(b) * d


def rotate_3d(x, y, z, a):
    """Simulate a 3D rotation (a in radians)"""
    return x, sin(a) * y + z * cos(a)


def d2_to_d3(x, y, z, r2d, r3d):
    """Apply the two rotations to get a 2D image of a 3D point."""
    x, y = rotate_2d(x, y, r2d)
    x, y = rotate_3d(x, y, z, r3d)
    return x + 192, y + 192/2


def draw_cube(r2d, r3d):
    # Draw each edges of a cube
    # from the lowest corner
    draw_line(d2_to_d3(-50, -50, -50, r2d, r3d), d2_to_d3(50, -50, -50, r2d, r3d), (255, 0, 0, 255))
    draw_line(d2_to_d3(-50, -50, -50, r2d, r3d), d2_to_d3(-50, 50, -50, r2d, r3d), (0, 255, 0, 255))
    draw_line(d2_to_d3(-50, -50, -50, r2d, r3d), d2_to_d3(-50, -50, 50, r2d, r3d), (0, 0, 255, 255))

    # from the highest corner
    draw_line(d2_to_d3(50, 50, 50, r2d, r3d), d2_to_d3(-50, 50, 50, r2d, r3d), (255, 0, 0, 255))
    draw_line(d2_to_d3(50, 50, 50, r2d, r3d), d2_to_d3(50, -50, 50, r2d, r3d), (0, 255, 0, 255))
    draw_line(d2_to_d3(50, 50, 50, r2d, r3d), d2_to_d3(50, 50, -50, r2d, r3d), (0, 0, 255, 255))

    # Other edges
    draw_line(d2_to_d3(-50, -50, 50, r2d, r3d), d2_to_d3(-50, 50, 50, r2d, r3d), (0, 255, 0, 255))
    draw_line(d2_to_d3(-50, -50, 50, r2d, r3d), d2_to_d3(50, -50, 50, r2d, r3d), (255, 0, 0, 255))

    draw_line(d2_to_d3(-50, 50, -50, r2d, r3d), d2_to_d3(50, 50, -50, r2d, r3d), (255, 0, 0, 255))
    draw_line(d2_to_d3(-50, 50, -50, r2d, r3d), d2_to_d3(-50, 50, 50, r2d, r3d), (0, 0, 255, 255))

    draw_line(d2_to_d3(50, -50, -50, r2d, r3d), d2_to_d3(50, 50, -50, r2d, r3d), (0, 255, 0, 255))
    draw_line(d2_to_d3(50, -50, -50, r2d, r3d), d2_to_d3(50, -50, 50, r2d, r3d), (0, 0, 255, 255))


print_test()
csp.test += 'test'
print_test()

for i in range(1000):
    clear_screen()
    draw_cube(i/100, R_3D)
    show_screen()
    sleep(0.01)
