#!/usr/bin/env python

import Image, ImageDraw
import simpleyaml as yaml
import argparse
from black_and_white import as_black_and_white

def bb(x, y, w, h):
    return (x, y, x + w, y + h)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('mean_file_yml')
    parser.add_argument('output')
    parser.add_argument('-split', type=int)
    args = parser.parse_args()
    meta_data = yaml.load(open(args.mean_file_yml))
    rows = 0
    max_w = 0
    max_h = 0
    for name, data in meta_data.items():
        rows += 1
        data['image'] = Image.open(data['path'])
        data['template'] = Image.open(data['template_path'])
        if args.split:
            data['image'] = as_black_and_white(data['image'], args.split, contrast=True)
            data['template'] = as_black_and_white(data['template'], args.split, contrast=True)
        max_w = max(max_w, data['template'].size[0])
        max_h = max(max_h, data['template'].size[1])
        max_w = max(max_w, data['image'].size[0])
        max_h = max(max_h, data['image'].size[1])

    width = max_w * 2
    height = rows * max_h
    pad = 5
    out = Image.new('RGBA', (width + 2 * pad, height + 2 * pad), "white")

    for i, (name, data) in enumerate(meta_data.items()):
        out.paste(data['template'], bb(pad, pad + i * max_h, max_w, max_h))
        out.paste(data['image'], bb(max_w + pad, pad + i * max_h, max_w, max_h))

    draw = ImageDraw.Draw(out)
    colour = '#F00'
    for i in range(1, rows):
        draw.line((0, i * max_h + pad, 2 * (pad + max_w), i * max_h + pad), fill=colour)
    draw.line((max_w + pad, 0, max_w + pad, max_h * rows + 2 * pad), fill=colour)
    del draw
    out.save(args.output)
