#!/usr/bin/env python

import matplotlib.pyplot as plt
import sys
import csv


def main(featurefile, classfile):
    feature_set = dict()
    class_data = [[sym for sym in row] for row in csv.reader(open(classfile))]
    feature_data = csv.DictReader(open(featurefile))

    for features in feature_data:
        for key, value in features.items():
            if key not in ['i', 'j']:
                sym = class_data[int(features['i'])][int(features['j'])]
                if key in feature_set:
                    if sym in feature_set[key]:
                        feature_set[key][sym].append(value)
                    else:
                        feature_set[key][sym] = [value]
                else:
                    feature_set[key] = {sym:[value]}

    for feature_name, data in feature_set.items():
        plt.title(feature_name)
        for symbol, points in data.items():
            plt.plot(points)
        plt.savefig(feature_name + '.png')
        plt.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s CSVFEATURES CSVCLASS" % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])


