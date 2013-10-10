#!/usr/bin/env python

import sys
import os
import csv
from argparse import ArgumentParser

try:
    import Image
    import ImageFilter
except ImportError:
    print "need PIL installed: easy_install PIL"
    sys.exit(1)


def parse_args():
    parser = ArgumentParser(
        description="""
        Extracts 'feature' data from an image file using convolution filters.
        CIS*4780 Computational Intelligence, University of Guelph.
        Authors: Ryan Pattison, Douglas Anderson, Oliver Cook
        Notes: requires PIL 'easy_install PIL'
        """)

    parser.add_argument('image', help="A greyscale bitmap image file to process.")
    parser.add_argument('columns', type=int, help="The number of 'cells' along the x-dimension in the image file's grid.")
    parser.add_argument('rows', type=int, help="The number of 'cells' along the y-dimension in the image file's grid.")
    parser.add_argument('filters', nargs='+', help="CSV files containing square matrices (3x3 or 5x5) to use as a convolution filter")
    
    parser.add_argument('-o', help="output directory to write csv data to, default=stdout")
    parser.add_argument('-filtered_image', help="where to save the filtered output image, (default=no save file)")
    
    args = parser.parse_args()
    
    if args.columns <= 0 or args.rows <= 0:
        raise ValueError("rows and columns must be positive integers")
    
    image_name = args.image
    args.image = Image.open(image_name)
    
    # TODO: construct an output filename, filtered_image name,  if a directory is given ...
    
    return args


def read_filters(filenames):
    filters = []
    for filename in filenames:
        with open(filename, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            try:
                matrix = [[float(aij) for aij in row] for row in reader]
            except:
                raise ValueError("ill-formed matrix file, (not all floats) in: " + filename)
        if len(matrix) != 3 and len(matrix) != 5:
            raise ValueError("matrix must be square with a width of 3 or 5: " + filename)
        if not all(len(r) == len(matrix) for r in matrix):
            raise ValueError("matrix must be square, in: " + filename)
        print [x for row in matrix for x in row]
        f = ImageFilter.Kernel((len(matrix), len(matrix)), [x for row in matrix for x in row])
        filters.append(f)
    return filters


def apply_filters(image, filters):
    for f in filters:
        image = image.filter(f)
    return image


def bounding_box(x, y, w, h, inset=0)
    return [x + inset, y + inset, x + w - 2 * inset, y + h - 2 * inset]


def analyze(image):
    vector = list(image.getdata())
    matrix = [vector[x:x + image.size[0]] for x in xrange(0, len(vector), image.size[0])]
    return dict(data=len(matrix))


def main(image, rows, columns, filter_list, csv_output=sys.stdout):
    cell_w = image.size[0] / columns
    cell_h = image.size[1] / rows
    print image
    print filters
    print "Rows:\t", rows3 s
    print "Cols:\t", columns
    print "Cell Width:\t", cell_w
    print "Cell Height:\t", cell_h
    filtered_image = apply_filters(image, filter_list)

    stats_data = [list() * rows]
    for i in range(columns):
        for j in range(rows):
            bb = bounding_box(i * cell_w, j * cell_h, cell_w, cell_h)
            cell = image.crop(bb)
            stats_data[i][j] = analyze(cell)

    header_names = ['i', 'j'].extend(stats_data[0].keys())
    stats_writer = csv.writer(csv_output)  #  maybe DictWriter would be nicer here.
    stats_writer.writerow(header_names)
    for i in range(columns):
        for j in range(rows):
            row = [i, j]
            for k in header_names:
                row.append(data[i][j][k])
            stats_writer.writerow(row)


if __name__ == "__main__":
    try:
        args = parse_args()
        image = args.image
        filters = read_filters(args.filters)
        main(args.image, args.rows, args.columns, filters)
    except Exception as e:
        print e
        sys.exit(1)

