#!/usr/bin/env python

from argparse import ArgumentParser

import Image
import numpy as np

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('gold', help="the image to compare against")
    parser.add_argument('candidate', help="the image to compare")
    return parser.parse_args()


def compare_images(A, B):
    dataA = np.array(A.getdata())
    dataB = np.array(B.getdata())
    diff = (dataA - dataB) ** 2
    return diff.sum()


if __name__ == "__main__":
    options = parse_args()
    print compare_images(Image.open(options.gold), Image.open(options.candidate))
