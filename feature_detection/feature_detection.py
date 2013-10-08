#!/usr/bin/env python

import sys
import re
import os
import csv
from argparse import ArgumentParser

import Image

def parse_args():
    parser = ArgumentParser(
        description="""
        Extracts 'feature' data from an image file using convolution filters.
        CIS*4780 Computational Intelligence, University of Guelph.
        Authors: Ryan Pattison, Douglas Anderson, Oliver Cook
        Notes: requires PIL 'easy_install PIL'
        """)
    parser.add_argument('image', help="A bitmap image file to process.", type=Image.open)
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
        if len(matrix) % 2 != 1:
            raise ValueError("matrix must have an odd size in: " + filename)
        if not all(len(r) == len(matrix) for r in matrix):
            raise ValueError("matrix must be square, in: " + filename)
        filters.append(matrix)
    return filters


def validate_args():
    filter_list = []
    isNumber = re.compile("(\d)")
    isCsv = re.compile(r"^((-?\d*,-?\d*,)*-?\d*)$")

    if len(sys.argv) < 5:
        print "Usage: ./feature_detection.py IMAGE WIDTH HEIGHT FILTER [FILTER...]"
        sys.exit(-1)

    try:
        image  = Image.open(sys.argv[1]) # Check if image is a real bitmap image
        imageName = os.path.basename(os.path.realpath(sys.argv[1])).split(".")[0]
    except:
        print "Invalid input image. Must be a greyscale bitmap"
        sys.exit(-1)
    try:
        width  = int(isNumber.match(sys.argv[2]).group(1)) ## Check width is number
        height = int(isNumber.match(sys.argv[3]).group(1)) ## Check height is number
    except:
        print "Invalid width or height"
        sys.exit(-1)

    for i in range(4, len(sys.argv)):
        f = sys.argv[i]
        try:
            filter_name  = os.path.basename(os.path.realpath(f)).split(".")[0]
            r = open(f, "r")
            for line in r:
                l = isCsv.match(line)
                if l == None:
                    raise Exception("Invalid CSV File. A line does not match expression")
            r.close()
            # TODO check filter is a square csv file of same width and height
            filter_list.append(filter_name)
        except:
            print "Invalid filter file.", f, " Must be a odd-width square csv file of real numbers"
            sys.exit(-1)
    return([image, imageName, width, height, filter_list])


def main(image, imageName, width, height, filter_list):
    # Output stats about each cell
    outputFile = imageName + "-" + "-".join(filter_list) + ".csv"
    outputPath  = os.path.join(os.getcwd(), "output", outputFile)
    print "Image name :\t", imageName
    print "Filter List:\t", ",".join(filter_list)
    print "Output File:\t", outputFile

    if not os.path.exists(os.path.join(os.getcwd(),"output")):
        print "No output directory in working directory"
        sys.exit(-1);
    try:
        w = open(outputPath, "w")
    except:
        print "Could not output to", outputPath
        sys.exit(-1)

    print "\nWorking...\n"
    for i in range(0,width):
        for j in range(0,height):
            w.write(str(i)+","+str(j)+",0\n")
    print "Closing:\t", outputFile
    w.close()


if __name__ == "__main__":
    try:
        args = parse_args()
        filters = read_filters(args.filters)
    except Exception as e:
        print e
        sys.exit(1)

    #args = validate_args()
    #main(args[0],args[1],args[2],args[3], args[4])

