#!/usr/bin/env python

from argparse import ArgumentParser

import Image, ImageFilter
import numpy as np

import align_images

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('gold', help="the image to compare against")
    parser.add_argument('candidate', help="the image to compare")
    return parser.parse_args()


def compare_images(A, B, scale=.4, align=True):
    if align:
        Bmatch = align_images.align_to(A, B).convert('L')
    else:
        Bmatch = B.convert('L')
    A = A.convert('L')
    new_shape = (np.array(A.size) * scale).astype(int)
    A = A.resize(new_shape, Image.ANTIALIAS)
    Bmatch = Bmatch.resize(new_shape, Image.ANTIALIAS)
    Bmatch = Bmatch.filter(ImageFilter.BLUR)
    A = A.filter(ImageFilter.BLUR)
    dataA = np.array(A.getdata())
    dataB = np.array(Bmatch.getdata())
    diff = abs(dataA - dataB)
    return float(diff.sum()) / np.prod(new_shape)


if __name__ == "__main__":
    options = parse_args()
    print compare_images(Image.open(options.gold), Image.open(options.candidate))
