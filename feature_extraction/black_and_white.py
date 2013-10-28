#!/usr/bin/env python

from argparse import ArgumentParser

import ImageOps
import Image

from greyscale import as_greyscale

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('-split_point', type=int, default=128)
    parser.add_argument('--auto_contrast', action="store_true")
    return parser.parse_args()


def as_black_and_white(image, split_point=128):
    image = as_greyscale(image)
    image = Image.eval(image, lambda px: 0 if px < split_point else 256)
    return image.convert('1', dither=Image.NONE)


if __name__ == "__main__":
    options = parse_args()
    image = Image.open(options.input)
    if options.auto_contrast:
        image = ImageOps.autocontrast(image)
    as_black_and_white(image, options.split_point).save(options.output)
