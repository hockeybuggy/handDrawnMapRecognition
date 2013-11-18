#! /usr/bin/env python

import sys
import csv


def rows_cols(csvfile):
    d = [x for x in csv.reader(open(csvfile))]
    return len(x), len(d[0])


def celldims(size, rows, cols):
    return int(round(float(size[0]) / cols)), int(round(float(size[1]) / rows))


if __name__ == "__main__":
    d = rows_cols(sys.argv[1])
    print d[0], d[1]
