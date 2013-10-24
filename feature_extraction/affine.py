#! /usr/bin/env python

import numpy as np

def identity():
    return np.array(
        [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]], dtype=float)


def rotation(angle):
    sa = np.sin(angle)
    ca = np.cos(angle)
    return np.array([
        [ca, -sa, 0],
        [sa, ca, 0],
        [0,  0, 1]
    ], dtype=float)


def translation(tx, ty):
    return np.array([
        [1, 0, 0],
        [0, 1, 0],
        [tx, ty, 1]
    ], dtype=float)


def scale(sx, sy=None):
    sy = sy or sx
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)


def multiply(*args):
    res = args[0]
    for A in args[1:]:
        res = res.dot(A)
    return res


def transform(dx, dy, stdrx, stdry, da):
    return multiply(translation(dx, dy), scale(stdrx, stdry), rotation(da))


def point(x, y):
    return np.array([x, y, 1], dtype=float)


def applytopoint(matrix, point):
    return point.dot(matrix)


def vars(b):
    """
    return the coefficients in the form which PIL likes.
    """
    a = np.array(np.matrix(b).I)
    return [a[0][0], a[1][0], a[2][0], a[0][1], a[1][1], a[2][1]]
