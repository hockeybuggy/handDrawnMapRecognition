#! /usr/bin/env python

import Image
import affine
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
    parser.add_argument("-bkg", type=str, help="background colour for pixels not in the original image", default="white")
    return parser.parse_args()


def transform_image(image, affine, bkg="white"):
    image = image.convert('RGBA') # add an alpha layer
    result = image.transform(image.size, Image.AFFINE, affine.vars(affine))
    output = Image.new('RGBA', image.size[:2], bkg)
    output.paste(result, (0, 0), result) # make sure the background is white
    return output


def affine_transform(ox=0, oy=0, sx=1, sy=1, a=0, tx=0, ty=0):
    return affine.multiply(
        affine.translation(-ox, -oy), # put origin at (0, 0)
        affine.rotation(a), # (rotate)
        affine.scale(sx, sy), # scale image
        affine.translation(ox, oy), # translate origin back to top left
        affine.translation(tx, ty)) # move to new position


if __name__ == "__main__":
    options = parse()
    matrix = affine_transform(
        ox=options.ox, oy=options.oy,
        sx=options.sx, sy=options.sy,
        a=options.a,
        tx=options.tx, ty=options.ty)
    image = Image.open(options.input)
    output = transform_image(image, matrix, options.bkg)
    output.save(options.output)


