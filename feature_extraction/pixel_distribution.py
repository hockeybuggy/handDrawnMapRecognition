#!/usr/bin/env python

import math
import sys
from argparse import ArgumentParser

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

from greyscale import as_greyscale


# TODO: weigh points based on value and get rid of black_points
def stats(black_points):
    xs = [x for x, y in black_points]
    ys = [y for x, y in black_points]
    c_x = np.mean(xs)
    c_y = np.mean(ys)
    std_x = np.std(xs)
    std_y = np.std(ys)

    a_sum = 0
    count = 0

    for x, y in black_points:
        dx = x - c_x
        dy = y - c_y
        a = math.atan2(dy, dx)
        a_sum += a
        count += 1

    ex_a = a_sum / count

    return c_x, c_y, std_x, std_y, ex_a


def black_points(image_name, thresh=127):
    points = []
    image = as_greyscale(Image.open(image_name))
    data = np.array(image.getdata())
    data.shape = image.size[:2]
    width, height = image.size[:2]
    for x in range(width):
        for y in range(height):
            if data[x][y] < thresh:
                points.append((y, x))
    return points


if __name__ == "__main__":
    print "mean-x, mean-y, std-x, std-y, mean-angle"
    for image in sys.argv[1:]:
        print ','.join(map(str, stats(black_points(image))))
