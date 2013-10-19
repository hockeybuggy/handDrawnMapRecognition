#!/usr/bin/python
import sys
import os
from shutil import rmtree
from itertools import permutations
from subprocess import call, check_call
from argparse import ArgumentParser
import multiprocessing as mp

def parse_args():
    parser = ArgumentParser( description="Calculates subsets of the set the equal the sum.")
    parser.add_argument("image", type=str, help="A greyscale bitmap image of a map")
    parser.add_argument("width", type=int, help="The width of the map in cell")
    parser.add_argument("height", type=int, help="The height of the map in cell")
    parser.add_argument("intended", type=str, help="A csv file of the intend representation")

    parser.add_argument('--output', help="""
        output file or directory to write csv data to.
        If directory file will be written in the form of: <dir name>/<image name>.csv
        default=<current working directory>/<image_name>.csv""")
    parser.add_argument('--tmpdir', default="tmp/", help="""
        output file or directory to write intermediate csv data to: default=tmp/""")
    parser.add_argument("--keeptmp", dest="keeptmp", action="store_true", default=False, help="""
        Remove intermediate csv files. default=false""")

    parser.add_argument("--noblur", dest="blur", action="store_false", default=True, help="""
        Apply blur filter to cell images. default=true""")
    parser.add_argument("--onlyblur", dest="onlyblur", action="store_true", default=False, help="""
        Do not collect results for unfilted images. default=false""")
    parser.add_argument("--permlen", type=int, default=2, help="""
        The permuation length of the filters. default=2""")

    args = parser.parse_args()
    if os.path.basename(os.getcwd()) != "handDrawnMapRecognition":
        raise Exception("Must be in root directory of the project")
    if os.path.exists(os.path.join(os.getcwd(),args.tmpdir)):
        raise Exception("Please clean up tmp dir. Exiting")
    if not args.output:
        args.output = os.path.join(os.getcwd(), os.path.basename(args.image).split(".")[0]+".csv")
    elif os.path.isdir(args.output):
        args.output = os.path.join(args.output, os.path.basename(args.image).split(".")[0]+".csv")
    return(args)

def map_pivot(args):
    call(["python", "scripts/map_csv_pivot.py"] + args)

def csv_join(files, output):
    w = open(output, "w")
    call(["python", "scripts/csv_join.py"]+files, stdout=w)
    w.close()

def get_filter_lists(permlen, blur, onlyblur):
    """
    Creates a list of filters be be applied s.t. main can simply loop though them.
    """
    filter_dir = "feature_extraction/filters/"
    idenity_filter = "iden"
    filters = ["horz", "vert", "dia1", "dia2"]
    blur_path = os.path.join(filter_dir,"lblur.csv")
    lists = []
    # Apply the idenity filter
    if not onlyblur:
        lists.append([os.path.join(filter_dir,idenity_filter+".csv")])
    if blur or onlyblur:
        lists.append([blur_path]+[os.path.join(filter_dir,idenity_filter+".csv")])
    # Apply all permutions of filters for perutation length r
    for r in range(1,permlen+1):
        for perm in permutations(filters,r):
            if not onlyblur:
                lists.append([os.path.join(filter_dir,f+".csv") for f in perm])
            if blur or onlyblur:
                lists.append([blur_path]+[os.path.join(filter_dir,f+".csv") for f in perm])
    return lists

def extract(filter_list):
    print "Extracting features under:", " and ".join([os.path.basename(f).split(".")[0] for f in filter_list])
    check_call(["python", "feature_extraction/feature_extraction.py"]+[extract.image,extract.width,extract.height]+filter_list+["-output",extract.tmpdir])

def init_filter_queue(q, image, width, height, tmpdir):
    extract.q = q
    extract.image = image
    extract.width = width
    extract.height = height
    extract.tmpdir = tmpdir

def main(image, width, height, intended, output, tmpdir, keeptmp, blur, onlyblur, permlen):
    os.mkdir(tmpdir)

    filter_lists = get_filter_lists(permlen, blur, onlyblur)
    filter_queue = mp.Queue()
    for filter_list in filter_lists:
        filter_queue.put(filter_list)
    pool = mp.Pool(None, init_filter_queue, [filter_queue, image, width, height, tmpdir])
    reqults = pool.imap(extract, filter_lists)
    pool.close()
    pool.join()

    print "Transforming intended csv"
    map_pivot([intended, tmpdir+"intended.csv"])

    print "Joining all intermediate csv files"
    csv_files = [tmpdir+csv_file for csv_file in os.listdir(tmpdir)]
    csv_join(csv_files, output)

    if not keeptmp:
        print "Removing intermediate csv files"
        rmtree(os.path.join(os.getcwd(),tmpdir))

if __name__ == "__main__":
    args = parse_args()
    main(args.image, str(args.width), str(args.height), args.intended, args.output,\
        args.tmpdir, args.keeptmp, args.blur, args.onlyblur, args.permlen)

