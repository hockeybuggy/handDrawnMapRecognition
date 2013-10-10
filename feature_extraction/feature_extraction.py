#!/usr/bin/env python

import sys
import re
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
        CIS*4780 Computational Intelligence, University of Guelph.str()j
        Authors: Ryan Pattison, Douglas Anderson, Oliver Cook
        Notes: requires PIL 'easy_install PIL'
        """)
    parser.add_argument('image',  type=Image.open, help="A greyscale bitmap image file to process.")
    parser.add_argument('columns', type=int, help="The number of 'cells' along the x-dimension in the image file's grid.")
    parser.add_argument('rows', type=int, help="The number of 'cells' along the y-dimension in the image file's grid.")
    parser.add_argument('filters', nargs='+', help="CSV files containing odd, square matrices to use in convolution filters")
    args = parser.parse_args()
    return args


def read_filters(filenames):
    filters = []
    for filename in filenames:
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            try:
                matrix = [[float(aij) for aij in row] for row in reader]
            except:
                raise ValueError("ill-formed matrix file, (not all floats) in: " + filename)
        if len(matrix) != 3  and len(matrix) != 5:
            raise ValueError("matrix must be square with a width of 3 or 5: " + filename)
        if not all(len(r) == len(matrix) for r in matrix):
            raise ValueError("matrix must be square, in: " + filename)
        print [x for row in matrix for x in row]
        f = ImageFilter.Kernel((len(matrix),len(matrix)), [x for row in matrix for x in row])
        filters.append(f)
    return filters

def apply_filters(image, filters):
    for f in filters:
        image = image.filter(f)
    return(image)

def get_cell_stats(cell):
    vector = list(cell.getdata())
    matrix = [vector[x:x+cell.size[0]] for x in xrange(0, len(vector),cell.size[0])]
    return [len(matrix)]
    

def main(image, rows, columns, filter_list):
    cell_w = image.size[0]/args.columns
    cell_h = image.size[1]/args.rows
    print image
    print filters
    print "Rows:\t", rows
    print "Cols:\t", columns
    print "Cell Width:\t", cell_w
    print "Cell Height:\t", cell_h
    filtered_image = apply_filters(image, filters)
    #filtered_image.save("test.bmp") # DEBUG

    w = open("OUTPUT.csv", "w")
    w.write("i,j\n")

    for i in range(0,columns):
        for j in range(0,rows):
            cell = filtered_image.crop([i*cell_w,j*cell_h,(i*cell_w)+cell_w,(j*cell_h)+cell_h])
            #cell.save("town" +str(i)+"-"+str(j)+".bmp") # DEBUG
            stats = get_cell_stats(cell)
            w.write(str(i)+","+str(j)+","+ ",".join(map(str, stats))+"\n")

    w.close()

if __name__ == "__main__":
    try:
        args = parse_args()
        image = args.image
        filters = read_filters(args.filters)
        main(args.image, args.rows, args.columns, filters)
    except Exception as e:
        print e
        sys.exit(1)

