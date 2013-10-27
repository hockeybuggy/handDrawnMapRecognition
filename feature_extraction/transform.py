#! /usr/bin/env python

import Image
from affine import *
from argparse import ArgumentParser

def parse():
    parser = ArgumentParser()
    parser.add_argument("input", help="image to transform")
    parser.add_argument("output", help="where to save transformed image")
    parser.add_argument("-tx", type=float, help="translation along the x axis to apply", default=0)
    parser.add_argument("-ty", type=float, help="translation along the y axis to apply", default=0)
    parser.add_argument("-sx", type=float, help="scale along the x axis to apply", default=1)
    parser.add_argument("-sy", type=float, help="scale along the y axis to apply", default=1)
    parser.add_argument("-a", type=float, help="angle in radians to rotate  (about the origin, counterclockwise) to apply", default=0)
    return parser.parse_args()


if __name__ == "__main__":
    options = parse()
    image = Image.open(options.input)
    affine = multiply(rotation(options.a), translation(options.tx, options.ty), scale(options.sx, options.sy))
    result = image.transform(image.size, Image.AFFINE, vars(affine))
    result.save(options.output)

