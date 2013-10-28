#!/usr/bin/env python

from argparse import ArgumentParser

import Image


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    return parser.parse_args()


def as_greyscale(image):
    if image.getbands() == ('L', ):
        return image
    else:
        return image.convert('L')


if __name__ == "__main__":
    options = parse_args()
    as_greyscale(Image.open(options.input)).save(options.output)
