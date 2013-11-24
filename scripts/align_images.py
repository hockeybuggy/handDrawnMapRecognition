#! /usr/bin/env python

import argparse
import math
import csv

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
    parser.add_argument("-transforms",
                        help="csv file to write transformations to (first, second, between)")
    parser.add_argument('-mark_align_to')
    parser.add_argument('-mark_transform')
    return parser.parse_args()


def bbcentre(x, y, w, h):
    tx = int(x - .5 * w)
    ty = int(y + .5 * h)
    lx = int(x + .5 * w)
    ly = int(y - .5 * h)
    return (tx, ly, lx, ty)


def draw_circle(draw, x, y, rx, ry=None, t=1, s=30, outline=(0, 0, 0)):
    da = math.pi * 2.0 / s
    if ry is None:
        ry = rx
    pts = [(math.cos(da * i) * rx + x, y + math.sin(da * i) * ry) for i in range(s)]
    for i in range(s - 1):
        a = pts[i]
        b = pts[i + 1]
        draw.line((a[0], a[1], b[0], b[1]), width=t, fill=outline)
    draw.line((pts[-1][0], pts[-1][1], pts[0][0], pts[1][1]), width=t, fill=outline)

def mark_align(image):
    stats = cal_align(image)
    image = image.convert('RGBA')
    draw = ImageDraw.Draw(image)
    W = 5
    r = 50
    c = (0, 255, 0)
    draw_circle(draw, stats[0], stats[1], rx=stats[2], ry=stats[3], t=W, outline=c)
    dx = np.cos(stats[4]) * r
    dy = np.sin(stats[4]) * r
    draw.line((stats[0], stats[1], stats[0] + dx, stats[1] + dy), fill=c, width=W)
    box = bbcentre(stats[0], stats[1], 10, 10)
    draw.ellipse(box, fill=c)
    del draw
    return image


def cal_align(image):
    image = black_and_white.as_black_and_white(image)
    black = pixel_distribution.black_points(image)
    return pixel_distribution.stats(black)


def diff_align(to, from_):
    cx = from_[0]
    cy = from_[1]
    tx = to[0] - cx
    ty = to[1] - cy
    assert(from_[2] != 0 and from_[3] != 0)
    sx = to[2] / from_[2]
    sy = to[3] / from_[3]
    #s = 0.5 * (sx + sy)
    ai = from_[4]
    aa = to[4]
    a = math.acos(np.sin(aa) * np.sin(ai) + np.cos(aa) * np.cos(ai))
    return cx, cy, sx, sy, a, tx, ty


def align_to(align_image, input_image, ignore_angle=True):
    diff = list(diff_align(cal_align(align_image), cal_align(input_image)))
    if ignore_angle:
        diff[4] = 0
    aff = transform.affine_transform(*diff)
    return transform.transform_image(input_image, aff)


if __name__ == "__main__":
    args = parse_args()
    match = Image.open(args.image_align_to)
    change = Image.open(args.image_transform)
    output = align_to(match, change)
    output.save(args.output)
    if args.transforms:
        with open(args.transforms, 'w') as f:
            c = csv.writer(f)
            from_ = cal_align(change)
            to = cal_align(match)
            c.writerow('cx cy sx sy a tx ty'.split())
            c.writerow(to + (0,0))
            c.writerow(from_ + (0,0))
            c.writerow(diff_align(to, from_))
    if args.mark_align_to:
        mark_align(match).save(args.mark_align_to)
    if args.mark_transform:
        mark_align(change).save(args.mark_transform)

