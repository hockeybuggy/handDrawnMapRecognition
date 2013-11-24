#!/usr/bin/env python

import sys
import math

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


def stats(black_points):
    xs = [x for x, y in black_points]
    ys = [y for x, y in black_points]
    c_x = np.mean(xs)
    c_y = np.mean(ys)
    std_x = np.std(xs)
    std_y = np.std(ys)

    sx = sy = 0
    for x, y in black_points:
        dx = (x - c_x)
        dy = (y - c_y)
        r = dx * dx + dy * dy
        sx += dx / r
        sy += dy / r
    ex_a = math.atan2(sy, sx)

    return c_x, c_y, std_x, std_y, ex_a


def black_points(image, thresh=127):
    points = []
    image = as_greyscale(image)
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
        print ','.join(map(str, stats(black_points(Image.open(image)))))
