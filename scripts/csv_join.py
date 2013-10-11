#!/usr/bin/python
import sys
import os
import csv

if len(sys.argv) < 2:
    print "Usage: ./scripts/csv_join.py CSV_FILES..."
    sys.exit(-1)

file_data = []
for csv_file in sys.argv[1:]:
    f = open(csv_file)
    r = csv.reader(f)
    data = {(row[0],row[1]): row[2:] for row in r}
    file_data.append(data)
    f.close()

final_data = dict()
for f in file_data:
    print f.keys()
    for key in  f.keys():
        if not final_data[key]:
            final_data[key] = []
        final_data[key].append(f[key])

f = open("output.csv", "w")
w = csv.writer(f)
w.writerows([[key[0], key[1], final_data[key]] for key in final_data])
