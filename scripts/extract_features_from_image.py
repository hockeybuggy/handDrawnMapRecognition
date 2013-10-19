#!/usr/bin/python
import sys
import os
from shutil import rmtree
from itertools import permutations
from subprocess import call
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser( description="Calculates subsets of the set the equal the sum.")
    parser.add_argument("image", type=str, help="A greyscale bitmap image of a map")
    parser.add_argument("width", type=int, help="The width of the map in cell")
    parser.add_argument("height", type=int, help="The height of the map in cell")
    parser.add_argument("intended", type=str, help="A csv file of the intend representation")
    parser.add_argument("--keeptmp", dest="keeptmp", action="store_true", default=False, help="A flag to control removal of intermediate files")
    # TODO add more args
    # TODO add blur
    # TODO add adjustable output
    # TODO add add filter list
    if os.path.basename(os.getcwd()) != "handDrawnMapRecognition":
        raise Exception("Must be in root directory of the project")
    if os.path.exists(os.path.join(os.getcwd(),"tmp")):
        raise Exception("Please clean up tmp dir. Exiting")
    return(parser.parse_args())

f_dir = "feature_extraction/filters/"
out_dir = "tmp/"

filters = ["horz", "vert", "dia1", "dia2"]

def feature_extraction(args):
    call(["python", "feature_extraction/feature_extraction.py"] + args)

def map_pivot(args):
    call(["python", "scripts/map_csv_pivot.py"] + args)

def csv_join(files, output):
    w = open(output, "w")
    call(["python", "scripts/csv_join.py"]+files, stdout=w)
    w.close()

def main(image, width, height, intended, keeptmp):
    os.mkdir(out_dir)

    for f in filters:
        print "Extracting features under: ", f
        feature_extraction([image, width, height,f_dir+f+".csv", "-output", out_dir])
    for combo in permutations(filters,2):
        print "Extracting features under: ", " and ".join(combo)
        feature_extraction([image, width, height,f_dir+combo[0]+".csv",f_dir+combo[1]+".csv","-output", out_dir])

    print "Transforming intended csv"
    map_pivot([intended, out_dir+"intended.csv"])

    print "Joining all intermediate csv files"
    csv_files = [out_dir+csv_file for csv_file in os.listdir(out_dir)]
    final_output = os.path.join(os.getcwd(), os.path.basename(image).split(".")[0]+".csv")
    csv_join(csv_files, final_output)

    if not keeptmp:
        print "Removing intermediate csv files"
        rmtree(os.path.join(os.getcwd(),out_dir))

if __name__ == "__main__":
    args = parse_args()
    main(args.image, str(args.width), str(args.height), args.intended, args.keeptmp)

