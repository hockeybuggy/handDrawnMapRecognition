#!/usr/bin/python
import sys
import csv
from argparse import ArgumentParser

import numpy as np
import simpleyaml as yaml


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
    parser.add_argument('-edge_class', default="EDGE", help="The name of the edge class, default=EDGE")
    parser.add_argument('save', help="yaml file to write to")
    parser.add_argument('-load', help="yaml file to read from")
    parser.add_argument('-probs', help="csvfile for probability maps")
    parser.add_argument('-min_n_size', type=int, default=15, help="""
        The minimum number of examples to be statistically valid, default=15 """)
    parser.add_argument('-map_classification_type', default="intended", help="""
        The method of creation of the input csv file. Either 'intended' or
        'classifier' recommenced. default='intended' """)

    args = parser.parse_args()
    return(args)


def get_neighbours(x, y, map_list, directions, edge_class):
    neighbours = dict()
    for direction in directions.keys():
        try:
            neighbour_pair = (x+directions[direction][0],y+directions[direction][1])
            if neighbour_pair[0] < 0 or neighbour_pair[1] < 0:
                raise IndexError() # do not allow negative indexing
            neighbours[direction] = get_class(neighbour_pair[0], neighbour_pair[1], map_list)
        except IndexError:
            neighbours[direction] = edge_class # If it's out of bounds assign edge class
    return neighbours


def get_class(x, y, map_list):
    return map_list[y][x]


def add_new_class_to_proximity_stats(prox_stats, new_class, directions):
    # Add new class to the other old classes
    for c_class in prox_stats.keys(): # add the new class to all of the previous keys
        for direction in directions:
            if new_class not in prox_stats[c_class][direction]:
                prox_stats[c_class][direction][new_class] = 0
    # Add directions and all classes to new class
    if new_class not in prox_stats:
        prox_stats[new_class] = dict()
        for direction in directions:
            prox_stats[new_class][direction] = dict()
            for n_class in prox_stats.keys():
                prox_stats[new_class][direction][n_class] = 0
    return prox_stats


def get_dict_sum(stats, c_class, direction, n_class=None):
    ttl = 0 # Total number of
    if n_class is None:
        for n_class in stats[c_class][direction]:
            ttl += stats[c_class][direction][n_class]
    else:
        ttl = stats[c_class][direction][n_class]
    return ttl


def get_proximity_counts(map_list, edge_class, directions, proximity_stats=dict()):
    """ Returns dictionary in the form of:
          [cell_class][direction][neighbour_class] = count of occurrences"""
    add_new_class_to_proximity_stats(proximity_stats, edge_class, directions) # Add null class
    for  i in range(0, len(map_list)):
        for j in range(0,len(map_list[i])):
            cell_class = get_class(j, i, map_list)
            if cell_class not in proximity_stats: # class has not been encountered yet.
                add_new_class_to_proximity_stats(proximity_stats, cell_class, directions)
            neighbours = get_neighbours(j, i, map_list, directions, edge_class)
            for direction in neighbours:
                n_class = neighbours[direction]
                if n_class not in proximity_stats[cell_class][direction]:
                    add_new_class_to_proximity_stats(proximity_stats, n_class, directions)
                proximity_stats[cell_class][direction][n_class] += 1
    return proximity_stats


def calculate_probabilities(prox_counts, min_n_size, edge_class):
    """ Returns a dictionary in the form of:
            [cell_class][given_probability_of] = prob if a class in a direction given cell_class """
    prox_prob = dict()
    for c_class in prox_counts.keys():
        prox_prob[c_class] = dict()
        for direction in prox_counts[c_class]:
            prox_prob[c_class][direction] = dict()
            n_class_ttl = get_dict_sum(prox_counts, c_class, direction)
            for n_class in prox_counts[c_class][direction]:
                n_class_sum = get_dict_sum(prox_counts, c_class, direction, n_class)
                #if n_class_ttl >= min_n_size:
                if n_class_ttl:
                    prox_prob[c_class][direction][n_class] = n_class_sum / float(n_class_ttl)
                else:
                    prox_prob[c_class][direction][n_class] = 0
    return prox_prob


def csv_probs(prox_prob, map_classifcation_type):
    # Convert to a prettier format
    key_name = "prob_of_{}_{}_given_{}"
    prob_headers = dict()
    for c_class in prox_prob.keys():
        prob_headers[c_class] = dict()
        for direction in prox_prob[c_class].keys():
            for n_class in prox_prob[c_class][direction].keys():
                given_prob = prox_prob[c_class][direction][n_class]
                prob_headers[c_class][key_name.format(n_class, direction, map_classifcation_type)] = given_prob
    return prob_headers


def get_header_from_prox_prob(prox_prob):
    return prox_prob.get(prox_prob.keys()[0]).keys()


def classify_byprob(map_list, prox_prob, directions, edge_class):
    out = []
    rev = dict([(v, k) for k, v in directions.items()])
    order = sorted(prox_prob.keys())
    for i in range(len(map_list)):
        for j in range(len(map_list[i])):
            neighbours = get_neighbours(j, i, map_list, directions, edge_class)
            pp = np.array([1.0] * len(prox_prob.keys()), dtype=float)
            for d in directions:
                rd = directions[d]
                rd = rev[-rd[0], -rd[1]]
                probs = prox_prob[neighbours[d]][rd]
                pp *= np.array([probs[k] for k in order])
            out.append([i, j] +  list(pp) + [map_list[i][j]])
    return out


def main(map_csv, out_fd, edge_class, min_n_size, map_classifcation_type, save_prox=None, class_prob_csv=None):
    reader = csv.reader(open(map_csv, "r"))
    writer = csv.writer(out_fd)
    directions = {'north':(0,1),'east':(1,0),'south':(0,-1),'west':(-1,0)}
    map_list = [ row for row in reader] # read file into array of arrays
    if save_prox is None:
        save_prox = dict()
    proximity_counts = get_proximity_counts(map_list, edge_class, directions, proximity_stats=save_prox)
    proximity_prob = calculate_probabilities(proximity_counts, min_n_size, edge_class)
    if class_prob_csv:
        classprobs = classify_byprob(map_list, proximity_prob, directions, edge_class)
        with open(class_prob_csv, 'w') as f:
            w = csv.writer(f)
            w.writerow(["i", "j"] + proximity_prob.keys() + ["intended"])
            for r in classprobs:
                w.writerow(r)
    prob_headers = csv_probs(proximity_prob, map_classifcation_type)
    header_names = ["i", "j", map_classifcation_type] + get_header_from_prox_prob(prob_headers)
    writer.writerow(header_names)
    for  i in range(0, len(map_list)):
        for j in range(0,len(map_list[i])):
            cell_class = get_class(j, i, map_list)
            writer.writerow([i, j, cell_class]+prob_headers[cell_class].values())


if __name__ == "__main__":
    args = parse_args()
    if args.output:
        out_fd = open(args.output, "w")
    else:
        out_fd = sys.stdout
    prox=dict()
    if args.load:
        prox=yaml.load(open(args.load))
    main(args.map_csv, out_fd, args.edge_class, args.min_n_size, args.map_classification_type, save_prox=prox, class_prob_csv=args.probs)
    if args.save:
        open(args.save, 'w').write(yaml.dump(prox))
