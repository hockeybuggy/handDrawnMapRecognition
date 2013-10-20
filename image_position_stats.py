#!/usr/bin/env python

import math
import sys
#from argparse import ArgumentParser

try:
    import Image
except ImportError:
    print "PIL package required: easy_install PIL"
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print "Numpy package required: easy_install Numpy"
    sys.exit(1)


# TODO: weigh points based on value and get rid of black_points
def stats(black_points):
    xs = [x for x, y in black_points]
    ys = [y for x, y in black_points]
    c_x = np.mean(xs)
    c_y = np.mean(ys)
    std_x = np.std(xs)
    std_y = np.std(ys)

    a_sum = 0
    r2_sum = 0

    for x, y in black_points:
        dx = x - c_x
        dy = y - c_y
        a = math.atan2(dy, dx)
        r2 = dx * dx + dy * dy
        a_sum += a * r2
        r2_sum += r2

    ex_a = a_sum / r2_sum

    return c_x, c_y, std_x, std_y, ex_a


def black_points(image_name, thresh=127):
    points = []
    image = Image.open(image_name)
    data = np.array(image.getdata())
    data.shape = image.size[:2]
    width, height = image.size[:2]
    for x in range(width):
        for y in range(height):
            if data[x][y] > thresh:
                points.append((x, y))
    return points


# TODO: output a transformed version of the image
def transform(A, B):
    fx, fy, fsx, fsy, fa = stats(A)
    tx, ty, tsx, tsy, ta = stats(B)
    nx = lambda x: (tx - fx) + cos(ta - fa) * (fsx / tsx) * (x - fx)
    ny = lambda y: (ty - fy) + sin(ta - fa) * (fsy / tsy) * (y - fy)
    return nx, ny


if __name__ == "__main__":
    print "mean-x, mean-y, std-x, std-y, mean-angle"
    for image in sys.argv[1:]:
        print ','.join(map(str, stats(black_points(image))))
