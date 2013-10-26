#!/usr/bin/python
import sys
import os
import csv
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(
        description="""
        Extracts proximity statistics of a csv file representing a map.
        CIS*4780 Computational Intelligence, University of Guelph.
        Authors: Ryan Pattison, Douglas Anderson, Oliver Cook
        Notes: requires PIL 'easy_install PIL'
        """)

    parser.add_argument('map_csv', help="A csv file representing a map.")
    parser.add_argument('-output', help="output file or directory to write csv data to, default=stdout")

    args = parser.parse_args()
    return(args)

def get_neighbors(x, y, map_list):
    neighbors = []
    mods = [(0,1),(1,0),(0,-1),(-1,0)]
    for direction in range(0,len(mods)):
        neighbors.append(get_class())
        
def get_class(x, y, map_list):
    return map_list[y][x]

def main(map_csv, out_fd):
    r = csv.reader(open(map_csv, "r"))
    w = csv.writer(out_fd)
    #i = 0
    map_list = []
    for row in r:
        map_list.append(row)

    w.writerow(["i", "j", "intended"])
    for  i in range(0, len(map_list)):
        for j in range(0,len(map_list[i])):
            cell_class = get_class(j, i, map_list)
            # TODO get neighbors
            w.writerow([i, j, cell_class])

if __name__ == "__main__":
    args = parse_args()
    if args.output:
        #try:
        out_fd = open(args.output, "w")
        #except:
            #raise Exception("Error. Could not open output for writing")
    else:
        out_fd = sys.stdout
    main(args.map_csv, out_fd)
