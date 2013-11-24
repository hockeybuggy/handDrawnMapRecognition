#!/usr/bin/python
import sys
import os
import csv

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(
        description="""
        Takes a csv map of symbols and outputs a pivoted version of it.
        Extracts proximity statistics of a csv file representing a map.
        CIS*4780 Computational Intelligence, University of Guelph.
        Authors: Ryan Pattison, Douglas Anderson, Oliver Cook
        Notes: requires PIL 'easy_install PIL'
        """)

    parser.add_argument('map_csv', help="A csv file representing a map.")
    parser.add_argument('-output', help="output file or directory to write csv data to, default=stdout")
    parser.add_argument('-label', default="intended", help="""
        The label of the value for each cell of the map csv file. Either 'intended' or
        'classifier' recommenced. default='intended' """)

    args = parser.parse_args()
    return(args)

def get_class(x, y, map_list):
    return map_list[y][x]

def main(map_csv, out_fd, label):
    reader = csv.reader(open(map_csv, "r"))
    writer = csv.writer(out_fd)

    map_list = [ row for row in reader] # read file into array of arrays

    header_names = ["i", "j", label]
    writer.writerow(header_names)

    for  i in range(0, len(map_list)):
        for j in range(0,len(map_list[i])):
            cell_class = get_class(j, i, map_list)
            writer.writerow([i, j, cell_class])

if __name__ == "__main__":
    args = parse_args()
    if args.output:
        out_fd = open(args.output, "w")
    else:
        out_fd = sys.stdout
    main(args.map_csv, out_fd, args.label)
