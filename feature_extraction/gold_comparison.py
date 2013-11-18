#!/usr/bin/env python

import argparse
import csv

import Image
import simpleyaml as yaml

import dims
from compare_images import compare_images
from black_and_white import as_black_and_white

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='grid to classify')
    parser.add_argument('rows', type=int, help='the number of rows in the grid')
    parser.add_argument('cols', type=int, help='the number of columns in the grid')
    parser.add_argument('gold', help='a yaml file of class: mean_image')
    parser.add_argument('output_csv', help='best guess at intended csv')
    parser.add_argument('-output_features', help='i, j, error1, ... in csv')
    parser.add_argument('-intended_csv', help='compare against these')
    parser.add_argument('--noalign', action="store_true", default=False, help='')
    parser.add_argument('-split', type=int)
    return parser.parse_args()


def gold_classify(gold_images, cell_image, align=True):
    return [(compare_images(gold, cell_image, align=False), className) for className, gold in gold_images.items()]


def bounding_box(x, y, w, h, inset=7):
    return (x + inset, y + inset, x + w - 2 * inset, y + h - 2 * inset)


if __name__ == "__main__":
    args = parse_args()
    grid = Image.open(args.image)
    cell_w, cell_h = dims.celldims(grid.size, args.rows, args.cols)
    answer = []

    gold = yaml.load(open(args.gold))
    for name, mean_img in gold.items():
        if 'path' in mean_img:
            gold[name] = Image.open(mean_img['path'])
        else:
            gold[name] = Image.open(mean_img)
        if args.split:
            gold[name] = as_black_and_white(gold[name], args.split, contrast=True)

    class_errs = [[gold_classify(gold,
                grid.crop(bounding_box(
                    j * cell_w, i * cell_h, cell_w, cell_h)))
                    for j in range(args.cols)] for i in range(args.rows)]

    if args.output_features:
        with open(args.output_features, 'w') as w:
            write = csv.writer(w)
            write.writerow(['i', 'j'] + list(gold.keys()))
            for i in range(args.rows):
                for j in range(args.cols):
                    write.writerow([float(i) / args.rows, float(j) / args.cols] + [x[0] for x in class_errs[j][i]])

    output = [[min(class_errs[i][j])[1] for j in range(args.cols)] for i in range(args.rows)]

    with open(args.output_csv, 'w') as out:
        write = csv.writer(out)
        for row in output:
            write.writerow(row)

    if args.intended_csv:
        diff = 0
        with open(args.intended_csv) as f:
            intended = csv.reader(f)
            for answer, guess in zip(intended, output):
                for a, b in zip(answer, guess):
                    if a != b:
                        diff += 1
        print diff
