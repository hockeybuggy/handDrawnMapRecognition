#! /usr/bin/env python

import argparse

import Image
import ImageDraw
import numpy as np

import pixel_distribution
import black_and_white
import transform


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_align_to',
                        help="copy the orientation etc. of this image")
    parser.add_argument('image_transform',
                        help="copied and transformed to match first image")
    parser.add_argument('output',
                        help="path to write the transformed image to")
    return parser.parse_args()


def bbcentre(x, y, w, h):
    tx = int(x - .5 * w)
    ty = int(y + .5 * h)
    lx = int(x + .5 * w)
    ly = int(y - .5 * h)
    return (tx, ly, lx, ty)


def mark_stats(image):
    image = black_and_white.as_black_and_white(image)
    black = pixel_distribution.black_points(image)
    stats = pixel_distribution.stats(black)
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    box = bbcentre(stats[0], stats[1], 10, 10)
    draw.ellipse(box, fill=(255, 0, 0) )
    box = bbcentre(stats[0], stats[1], 2 * stats[2], 2 * stats[3])
    draw.ellipse(box, outline=(255, 0, 0) )
    r = 50
    dx = np.cos(stats[4]) * r
    dy = np.sin(stats[4]) * r
    draw.line((stats[0], stats[1], stats[0] + dx, stats[1] + dy), fill=(0, 0, 255))
    del draw
    return image


def align_to(align_image, input_image):
    original = input_image
    align_image = black_and_white.as_black_and_white(align_image)
    input_image = black_and_white.as_black_and_white(input_image)
    ablack = pixel_distribution.black_points(align_image)
    iblack = pixel_distribution.black_points(input_image)
    astat = pixel_distribution.stats(ablack)
    istat = pixel_distribution.stats(iblack)
    cx = istat[0]
    cy = istat[1]
    tx = astat[0] - cx
    ty = astat[1] - cy
    sx = astat[2] / istat[2]
    sy = astat[3] / istat[3]
    s = .5 * (sx + sy)
    a = istat[4] - astat[4]
    aff = transform.affine_transform(cx, cy, s, s, a, tx, ty)
    return transform.transform_image(original, aff)


if __name__ == "__main__":
    args = parse_args()
    match = Image.open(args.image_align_to)
    change = Image.open(args.image_transform)
    output = align_to(match, change)
    output.save(args.output)
    mark_stats(match).save('match.png')
    mark_stats(change).save('change.png')
