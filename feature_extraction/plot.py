#!/usr/bin/env python

import matplotlib.pyplot as plt
import simpleyaml as yaml
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s YAML FILE" % sys.argv[0]
        sys.exit(1)
    plt.plot(yaml.load(open(sys.argv[1]))[0][0]['x'])
    plt.savefig("output.png")
