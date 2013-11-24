#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import simpleyaml as yaml
import sys
import csv

def main(yamlfilename, csvfilename):
    vectors = yaml.load(open(yamlfilename))
    symbol_class = [[c for c in r] for r in csv.reader(open(csvfilename))]
    rows = len(vectors)
    cols = len(vectors[0])

    # sort the data by class
    by_class = dict()
    for i in range(rows):
        for j in range(cols):
            vec = vectors[i][j]
            sym = symbol_class[i][j]
            if sym in by_class:
                by_class[sym].append(vec)
            else:
                by_class[sym] = [vec]

    # plot the data as an average over the class
    for sym, vecs in by_class.items():
        for key in vecs[0].keys():
            pad = 2
            key_matrix = np.array([v[key][pad:-pad] for v in vecs])
            y = key_matrix.mean(0)
            x = range(pad, len(key_matrix[0]) + pad)
            err = key_matrix.std(0)
            plt.errorbar(x, y, yerr=err)
            name = "output-%s-%s--%d.png" % (sym, key, len(vecs))
            plt.title(name)
            plt.savefig(name)
            plt.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s YAMLFILE CSVFILE" % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])


