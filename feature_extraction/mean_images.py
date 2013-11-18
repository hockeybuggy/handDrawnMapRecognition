#!/usr/bin/env python

import argparse
import csv

import simpleyaml as yaml
import Image

import align_images


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('map', help='grid_image')
    parser.add_argument('intended', help='csv with class names')
    parser.add_argument('-gold', help="path to previously generated yaml")
    parser.add_argument('output', help="meta_data output path")
    parser.add_argument('--noalign', action='store_true', default=False, help="dont try to align to template")
    return parser.parse_args()


def bounding_box(x, y, w, h, inset=4):
    return (x + inset, y + inset, x + w - inset, y + h - inset)

if __name__ == "__main__":
    args = parse_args()
    if args.gold:
        meta_data = yaml.load(open(args.gold))
        for name, data in meta_data.items():
            meta_data[name]['image'] = Image.open(data['path'])
            meta_data[name]['template'] = Image.open(data['template_path'])
    else:
        meta_data = dict()

    grid = Image.open(args.map).convert('RGBA')
    classes = [r for r in csv.reader(open(args.intended))]

    rows = len(classes)
    cols = len(classes[0])
    width = grid.size[0] / cols
    height = grid.size[1] / rows

    for j in range(rows):
        for i in range(cols):
            name = classes[j][i]
            cell = grid.crop(bounding_box(i * width, j * height, width, height))
            if name in meta_data:
                data = meta_data[name]
                data['n'] += 1
                if not args.noalign:
                    cell = align_images.align_to(data['template'], cell)
                img = data['image']
                data['image'] = Image.blend(img, cell, 1.0 / data['n'])
            else:
                data = dict(image=cell, n=1,
                    path=name+'_mean.png',
                    template_path=name+'_temp_mean.png',
                    template=cell)
                meta_data[name] = data


    for name, data in meta_data.items():
        data['image'].save(data['path'])
        data['template'].save(data['template_path'])
        del data['image']
        del data['template']

    with open(args.output, 'w') as out:
        out.write(yaml.dump(meta_data))
