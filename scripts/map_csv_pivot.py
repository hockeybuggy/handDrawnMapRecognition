#!/usr/bin/python
import sys
import os
import csv

if len(sys.argv) == 4:
    print "Usage: ./scripts/map_csv_pivot.py CSV_MAP OUTPUT"
    sys.exit(-1)

r = csv.reader(open(sys.argv[1], "r"))
w = csv.writer(open(sys.argv[2], "w"))
i = 0

w.writerow(["i", "j", "intended"])
for row in r:
    for j in range(0,len(row)):
        w.writerow([i, j, row[j]])
    i+=1
