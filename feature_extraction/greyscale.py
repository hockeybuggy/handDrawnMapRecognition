#!/usr/bin/env python

from argparse import ArgumentParser

import Image


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    return parser.parse_args()


if __name__ == "__main__":
    options = parse_args()
    Image.open(options.input).convert('L').save(options.output)
