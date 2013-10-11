#!/usr/bin/python
import sys
import os
from itertools import permutations
from subprocess import call

if len(sys.argv) != 4 or os.path.basename(os.getcwd()) != "handDrawnMapRecognition":
    print "Usage: from repo root ./scripts/extract_features_from_image.py <IMAGE> <CELLS WIDE> <CELL HIGH>"
    sys.exit(-1)
if os.path.exists(os.getcwd()+"tmp"):
    print "Please clean up tmp dir. Exiting"
    sys.exit(-1)

filter_dir = "feature_extraction/filters/"
output_dir = "tmp/"
feature_extraction_exe = "feature_extraction/feature_extraction.py"

os.mkdir(output_dir)

filters = ["horz", "vert", "dia1", "dia2"]

for f in filters:
    print "Extracting features for under: ", f
    call(["python",feature_extraction_exe,sys.argv[1],sys.argv[2],sys.argv[3],filter_dir+f+".csv","-output",output_dir])

for combo in permutations(filters,2):
    print "Extracting features for under: ", " and ".join(combo)
    call(["python",feature_extraction_exe,sys.argv[1],sys.argv[2],sys.argv[3],filter_dir+combo[0]+".csv",filter_dir+combo[1]+".csv","-output",output_dir])

# TODO at this point this should join the csv files
