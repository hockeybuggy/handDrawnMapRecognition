#!/usr/bin/env python

from argparse import ArgumentParser

import Image


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('top_x', type=int)
    parser.add_argument('top_y', type=int)
    parser.add_argument('bottom_x', type=int)
    parser.add_argument('bottom_y', type=int)
    return parser.parse_args()


if __name__ == "__main__":
    options = parse_args()
    image = Image.open(options.input)
    image = image.crop((options.top_x, options.top_y, options.bottom_x, options.bottom_y))
    image.save(options.output)
