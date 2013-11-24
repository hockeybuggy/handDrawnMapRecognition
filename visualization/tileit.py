#!/usr/bin/env python

import csv
import argparse
import os

import simpleyaml as yaml
import Image


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tileset', help="directory with images and yaml file")
    parser.add_argument('csv_map', help="csv file to tileize")
    parser.add_argument('output', help="where to output image")
    return parser.parse_args()


def boundingbox(x, y, w, h):
    return (x, y, x + w, y + h)


if __name__ == "__main__":
    args = parse_args()
    tile_set = yaml.load(open(os.path.join(args.tileset, 'tiles.yml')))
    for name, data in tile_set.items():
        if name != 'tiles':
            tile_set[name]['image'] = Image.open(
                os.path.join(args.tileset, data['image']))
    classes = [r for r in csv.reader(open(args.csv_map))]
    
    width = tile_set['tiles']['width']
    height = tile_set['tiles']['height']
    output_size = (width * len(classes[0]), height * len(classes))
    output = Image.new('RGB', output_size, "white")

    old = [list(x) for x in classes]
    for j, row in enumerate(classes):
        for i, cell in enumerate(row):
            if cell and cell in tile_set:
                tile = tile_set[cell]
                bb = boundingbox(
                    i * width,
                    j * height,
                    tile['cols'] * width,
                    tile['rows'] * height)
                output.paste(tile['image'], bb)
                for di in range(tile['cols']):
                    for dj in range(tile['rows']):
                        if j + dj >= len(classes) or i + di >= len(classes[0]):
                            continue
                        other_cell = classes[j + dj][i + di]
                        if other_cell == None:
                            other_cell = old[j + dj][i + di]
                        if other_cell == cell:
                            classes[j + dj][i + di] = None
                        elif other_cell in tile_set:
                            other_tile = tile_set[other_cell]
                            bb = boundingbox(
                                (i + di) * width,
                                (j + dj) * height,
                                width * other_tile['cols'],
                                height * other_tile['rows'])
                            output.paste(other_tile['image'], bb)
                            
    
    output.save(args.output)
