#!/usr/bin/env python

import argparse

import Image, ImageDraw

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('map')
    parser.add_argument('rows', type=int)
    parser.add_argument('cols', type=int)
    parser.add_argument('output')
    args = parser.parse_args()
    grid = Image.open(args.map)
    cw = int(round(float(grid.size[0]) / args.cols))
    ch = int(round(float(grid.size[1]) / args.rows))
    draw = ImageDraw.Draw(grid)
    colour = '#F00'
    width = 3
    for i in range(args.cols):
        draw.line((cw * i, 0, cw * i, grid.size[1]), fill=colour, width=width)
    for i in range(args.rows):
        draw.line((0, ch * i, grid.size[0], ch * i), fill=colour, width=width)
    del draw
    grid.save(args.output)
