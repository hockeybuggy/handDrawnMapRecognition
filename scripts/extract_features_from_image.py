#!/usr/bin/python
import sys
import os
from shutil import rmtree
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
csv_join_exe = "scripts/csv_join.py"
final_output = os.path.join(os.getcwd(), os.path.basename(sys.argv[1]).split(".")[0]+".csv")
os.mkdir(output_dir)

filters = ["horz", "vert", "dia1", "dia2"]

for f in filters:
    print "Extracting features for under: ", f
    call(["python",feature_extraction_exe,sys.argv[1],sys.argv[2],sys.argv[3],filter_dir+f+".csv","-output",output_dir])

for combo in permutations(filters,2):
    print "Extracting features for under: ", " and ".join(combo)
    call(["python",feature_extraction_exe,sys.argv[1],sys.argv[2],sys.argv[3],filter_dir+combo[0]+".csv",filter_dir+combo[1]+".csv","-output",output_dir])

print "Joining all intermediate csv files"
csv_files = [output_dir+csv_file for csv_file in os.listdir(output_dir)]
w = open(final_output, "w")
call(["python",csv_join_exe]+csv_files, stdout=w)
w.close()

print "Removing intermediate csv files"
rmtree(os.path.join(os.getcwd(),output_dir))

