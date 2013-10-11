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
    for key in f.keys():
        try:
            final_data[key].extend(f[key])
        except KeyError:
            final_data[key] = f[key]

w = csv.writer(sys.stdout)

keys = final_data.keys()
header_key = keys.pop(keys.index(("i","j")))
sorted_keys = sorted(keys, cmp=lambda x,y: cmp((int(x[0]),int(x[1])),(int(y[0]),int(y[1]))) )

w.writerow([header_key[0], header_key[1]]+final_data[header_key])
w.writerows([[key[0], key[1]]+final_data[key] for key in sorted_keys])
