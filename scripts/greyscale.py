#!/usr/bin/env python

from argparse import ArgumentParser

import ImageOps
import Image


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--auto_contrast', action="store_true")
    return parser.parse_args()


def as_greyscale(image):
    if image.mode == 'L':
        return image
    else:
        return image.convert('L')


if __name__ == "__main__":
    options = parse_args()
    image = Image.open(options.input)
    if options.auto_contrast:
        image = ImageOps.autocontrast(image)
    as_greyscale(image).save(options.output)
