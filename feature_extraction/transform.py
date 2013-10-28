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
    parser.add_argument("-ox", type=float, help="x origin", default=0)
    parser.add_argument("-oy", type=float, help="y origin", default=0)
    parser.add_argument("-a", type=float, help="angle in radians to rotate  (about the origin, counterclockwise) to apply", default=0)
    return parser.parse_args()


def transform_image(image, affine):
    image = image.convert('RGBA') # add an alpha layer
    result = image.transform(image.size, Image.AFFINE, vars(affine))
    output = Image.new('RGBA', image.size[:2], 'white')
    output.paste(result, (0, 0), result) # make sure the background is white
    return output


if __name__ == "__main__":
    options = parse()
    affine = multiply(
        translation(-options.ox, -options.oy),
        rotation(options.a),
        scale(options.sx, options.sy),
        translation(options.ox, options.oy),
        translation(options.tx, options.ty))
    image = Image.open(options.input)
    output = transform_image(image, affine)
    output.save(options.output)


