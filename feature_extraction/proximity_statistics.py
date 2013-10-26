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


def get_neighbours(x, y, map_list, directions, null_class):
    neighbours = dict()
    for direction in directions.keys():
        try:
            neighbour_pair = (x+directions[direction][0],y+directions[direction][1])
            if neighbour_pair[0] < 0 or neighbour_pair[1] < 0:
                raise IndexError() # do not allow negative indexing
            neighbours[direction] = get_class(neighbour_pair[0], neighbour_pair[1], map_list)
        except IndexError:
            neighbours[direction] = null_class # Null class for edges
    return neighbours


def get_class(x, y, map_list):
    return map_list[y][x]


def add_new_class_to_proximity_stats(prox_stats, new_class, directions):
    # Add new class to the other old classes
    for c_class in prox_stats.keys(): # add the new class to all of the previous keys
        for direction in directions:
            prox_stats[c_class][direction][new_class] = 0
    # Add directions and all classes to new class
    prox_stats[new_class] = dict()
    for direction in directions:
        prox_stats[new_class][direction] = dict()
        for n_class in prox_stats.keys():
            prox_stats[new_class][direction][n_class] = 0
    return prox_stats

def get_dict_sum(stats, null_class, c_class, direction, n_class=None):
    ttl = 0.0 # Total number of 
    if n_class is None:
        for n_class in stats[c_class][direction]:
            if n_class != null_class:
                ttl += stats[c_class][direction][n_class]
    else:
        ttl = stats[c_class][direction][n_class]
    return ttl

def main(map_csv, out_fd):
    r = csv.reader(open(map_csv, "r"))
    w = csv.writer(out_fd)
    directions = {'n':(0,1),'e':(1,0),'s':(0,-1),'w':(-1,0)}
    null_class = "NULL"
    min_n_size = 15
    map_list = []
    for row in r:
        map_list.append(row)

    proximity_stats = dict() # [cell_class][direction][neighbour_class]
    add_new_class_to_proximity_stats(proximity_stats, null_class, directions) # Add null class
    for  i in range(0, len(map_list)):
        for j in range(0,len(map_list[i])):
            cell_class = get_class(j, i, map_list)
            if cell_class not in proximity_stats: # class has not been encountered yet.
                add_new_class_to_proximity_stats(proximity_stats, cell_class, directions)
            neighbours = get_neighbours(j, i, map_list, directions, null_class)
            for direction in neighbours:
                n_class = neighbours[direction]
                if n_class not in proximity_stats[cell_class][direction]:
                    add_new_class_to_proximity_stats(proximity_stats, n_class, directions)
                proximity_stats[cell_class][direction][n_class] += 1

    #for key in proximity_stats.keys():
        #print key, ":" 
        #for direct in proximity_stats[key]:
            #print direct, ":",  proximity_stats[key][direct]
        #print

    proximity_prob = dict()
    for c_class in proximity_stats.keys():
        if c_class != null_class:
            proximity_prob[c_class] = dict()
            for direction in proximity_stats[c_class]:
                proximity_prob[c_class][direction] = dict()
                n_class_ttl = get_dict_sum(proximity_stats, null_class, c_class, direction)
                for n_class in proximity_stats[c_class][direction]:
                    n_class_sum = get_dict_sum(proximity_stats, null_class, c_class, direction, n_class)
                    if n_class_ttl >= min_n_size:
                        proximity_prob[c_class][direction][n_class] = n_class_sum / n_class_ttl
                    else:
                        proximity_prob[c_class][direction][n_class] = None

    for key in proximity_prob.keys():
        print key, ":" 
        for direct in proximity_prob[key]:
            print direct, ":",  proximity_prob[key][direct]
        print

    header_names = ["i", "j", "intended"]
    w.writerow(header_names)
    for  i in range(0, len(map_list)):
        for j in range(0,len(map_list[i])):
            w.writerow([i, j, cell_class])


if __name__ == "__main__":
    args = parse_args()
    if args.output:
        out_fd = open(args.output, "w")
    else:
        out_fd = sys.stdout
    main(args.map_csv, out_fd)
