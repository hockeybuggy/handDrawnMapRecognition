#!/usr/bin/env python

import argparse
import csv

import Image
import simpleyaml as yaml

from compare_images import compare_images


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='grid to classify')
    parser.add_argument('rows', type=int, help='the number of rows in the grid')
    parser.add_argument('cols', type=int, help='the number of columns in the grid')
    parser.add_argument('gold', help='a yaml file of class: mean_image')
    parser.add_argument('output_csv', help='best guess at intended csv')
    parser.add_argument('-intended_csv', help='compare against these')
    return parser.parse_args()


def gold_classify(gold_images, cell_image):
    return min((compare_images(gold, cell_image), className)
        for className, gold in gold_images.items())[1]


def bounding_box(x, y, w, h):
    return (x, y, x + w, y + h)


if __name__ == "__main__":
    args = parse_args()
    grid = Image.open(args.image)
    print grid
    cell_w = grid.size[0] / args.cols
    cell_h = grid.size[1] / args.rows
    answer = []
    
    gold = yaml.load(open(args.gold))
    for name, mean_img in gold.items():
        gold[name] = Image.open(mean_img)
    
    output = [[gold_classify(gold,
                grid.crop(bounding_box(
                    j * cell_w, i * cell_h, cell_w, cell_h)))
                    for j in range(args.cols)] for i in range(args.rows)]
    
    with open(args.output_csv, 'w') as out:
        write = csv.writer(out)
        for row in output:
            write.writerow(row)
    
    if args.intended:
        diff = 0
        with open(args.intended) as f:
            intended = csv.reader(f)
            for answer, guess in zip(intended, output):
                for a, b in zip(answer, guess):
                    if a != b:
                        diff += 1
        print diff 
