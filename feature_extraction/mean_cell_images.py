#!/usr/bin/python
import sys
import os
import csv
from argparse import ArgumentParser

try:
    import Image
except ImportError:
    print "PIL package required: easy_install PIL"
    sys.exit(1)

import align_images

def parse_args():
    parser = ArgumentParser( description="Create an image with every example of each class in the map.")
    parser.add_argument("data", type=file, help="A csv file with the fields i, j, and intended")
    parser.add_argument("image_prefix", type=str, help="A str that allows you to specify which images are included")
    parser.add_argument("images", nargs="+", help="A list of cell images")
    parser.add_argument('-label', default="intended", help="The label of the class, default=intended")
    parser.add_argument('-output', help="output directory to write to mean images, default=<cwd>")
    args = parser.parse_args()
    images = []
    for image in args.images:
        images.append(Image.open(image))
    return (args.data, args.output, args.image_prefix, images, args.label)


def main(data_file, outdir, image_prefix, cell_images, label):
    images_by_class = dict()
    image_name = image_prefix + "_y{:02d}_x{:02d}.bmp"
    # read csv file
    r = csv.dictreader(data_file)
    for row in r:
        # Create lists of images from each class
        cell_image = Image.open(image_name.format(int(row["j"]), int(row["i"])))
        if row[label] in images_by_class: # make intended. not hard coded.
            images_by_class[row[label]].append(cell_image)
        else:
            images_by_class[row[label]] = [ cell_image ]

    for key in images_by_class:
        #print key, images_by_class[key], "\n"
        dilution = 1.0/float(len(images_by_class[key]))
        print key, "at a dilution of:", dilution
        # Create an image for each list of images
        mean_image = Image.new("L", images_by_class[key][0].size, "white")
        template = None
        for image in images_by_class[key]:
            if template:
                image = align_images.align_to(template, image)
            else:
                template = image
            mean_image = Image.blend(mean_image, image, dilution)
        mean_image.save(os.path.join(outdir,key+".bmp") if outdir else key+".bmp")


if __name__ == "__main__":
    main(*parse_args())

