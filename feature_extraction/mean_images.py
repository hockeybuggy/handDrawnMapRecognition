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


def blend_images(imgs):
    count = len(imgs)
    if not imgs:
        raise ValueError('Not images given to blend')
    if count == 1:
        return imgs[0]
    else:
        return Image.blend(blend_images(imgs[:count/2]), blend_images(imgs[count/2:]), .5)


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

    # collect all cells by class name
    img_by_class = dict()
    for j in range(rows):
        for i in range(cols):
            name = classes[j][i]
            cell = grid.crop(bounding_box(i * width, j * height, width, height))
            if name in img_by_class:
                img_by_class[name].append(cell)
            else:
                img_by_class[name] = [cell]

    # align all the images to the first
    for name, imgs in img_by_class.items():
        for i in range(1, len(imgs)):
            if not args.noalign:
                imgs[i] = align_images.align_to(imgs[0], imgs[i])

    # blend all the images
    for name, imgs in img_by_class.items():
        data = dict(
            template=imgs[0],
            image=blend_images(imgs),
            n=len(imgs))
        img_by_class[name] = data

    # update the meta_data and saved means
    for name, newdata in img_by_class.items():
        if name in meta_data:
            data = meta_data[name]
            data['n'] += newdata['n']
            cell = newdata['image']
            if not args.noalign:
                cell = align_images.align_to(data['template'], cell)
            img = data['image']
            data['image'] = Image.blend(img, cell, newdata['n'] / data['n'])
        else:
            meta_data[name] = dict(image=newdata['image'], n=newdata['n'],
                path=name+'_mean.png',
                template_path=name+'_temp_mean.png',
                template=newdata['template'])

    # write out images and remove PIL data
    for name, data in meta_data.items():
        data['image'].save(data['path'])
        data['template'].save(data['template_path'])
        del data['image']
        del data['template']

    with open(args.output, 'w') as out:
        out.write(yaml.dump(meta_data))