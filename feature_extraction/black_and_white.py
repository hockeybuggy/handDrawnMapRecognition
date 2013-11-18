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
    parser.add_argument('--auto_contrast', action="store_true", default=False)
    return parser.parse_args()



def as_black_and_white(image, split_point=128, contrast=False):
    image = as_greyscale(image)
    if contrast:
        image = ImageOps.autocontrast(image)
    image = Image.eval(image, lambda px: 0 if px < split_point else 255)
    return image.convert('1', dither=Image.NONE)


if __name__ == "__main__":
    args = parse_args()
    image = Image.open(args.input)
    as_black_and_white(image, args.split_point, args.auto_contrast).save(args.output)
