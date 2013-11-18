#! /usr/bin/env python

import sys
import csv

d = [x for x in csv.reader(open(sys.argv[1]))]
print len(x), len(d[0])
