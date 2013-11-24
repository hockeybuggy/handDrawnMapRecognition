#!/usr/bin/env python

from argparse import ArgumentParser

import Image
import ImageColor


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('search', type=ImageColor.getrgb, help='rgb hex string, without #')
    parser.add_argument('replace', type=ImageColor.getrgb)
    parser.add_argument('-tolerance', type=ImageColor.getrgb, default=(0, 0, 0))
    parser.add_argument('-fuzzy_factor', type=float, help="how much is based on current pixel, vs surrounding", default=1.0)
    return parser.parse_args()


def image_search_replace(image, red, green, blue, new_red, new_green, new_blue, tol_red=0, tol_green=0, tol_blue=0, fuzzy_factor=.85):
    pixels = image.load()
    search = (red, green, blue)
    replace = (new_red, new_green, new_blue)
    tolerance = (tol_red, tol_green, tol_blue)
    last_col = [0.0] * image.size[1]
    for x in range(image.size[0]):
        last_accept = 0
        for y in range(image.size[1]):
            pix = pixels[x, y]
            slack = max(abs(p - s) / float(t) for p, s, t in zip(pix, search, tolerance))
            acceptance = slack * fuzzy_factor + ((1 - fuzzy_factor) * (last_accept + last_col[y]) * .5)
            if acceptance < 1:
                pixels[x, y] = replace
            last_accept = acceptance
            last_col[y] = acceptance
    return image


if __name__ == "__main__":
    options = parse_args()
    image = Image.open(options.input)
    output = image_search_replace(
                         image,
                         options.search[0],
                         options.search[1],
                         options.search[2],
                         options.replace[0],
                         options.replace[1],
                         options.replace[2],
                         options.tolerance[0],
                         options.tolerance[1],
                         options.tolerance[2],
                         options.fuzzy_factor)
    output.save(options.output)
