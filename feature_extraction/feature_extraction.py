#!/usr/bin/env python

import sys
import os
import csv
from argparse import ArgumentParser
try:
    from yaml import dump as yaml_dump
except ImportError:
    def yaml_dump(d):
        raise ValueError("YAML required for yaml dumping: easy_install yaml")

try:
    import Image
    import ImageFilter
except ImportError:
    print "PIL package required: easy_install PIL"
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print "Numpy package required: easy_install Numpy"
    sys.exit(1)


def parse_args():
    parser = ArgumentParser(
        description="""
        Extracts 'feature' data from an image file using convolution filters.
        CIS*4780 Computational Intelligence, University of Guelph.
        Authors: Ryan Pattison, Douglas Anderson, Oliver Cook
        Notes: requires PIL 'easy_install PIL'
        """)

    parser.add_argument('image', help="A greyscale bitmap image file to process.")
    parser.add_argument('columns', type=int, help="The number of 'cells' along the x-dimension in the image file's grid.")
    parser.add_argument('rows', type=int, help="The number of 'cells' along the y-dimension in the image file's grid.")
    parser.add_argument('filters', nargs='+', help="CSV files containing square matrices (3x3 or 5x5) to use as a convolution filter")

    parser.add_argument('--save_map_image', dest='save_map_image', action='store_true', help="Save a copy of the post-filtered map")
    parser.add_argument('--save_cell_images', dest='save_cell_images', action='store_true', help="Save a copy of each of the post-filtered cells")
    parser.add_argument('-output', help="output file or directory to write csv data to, default=stdout")
    parser.add_argument('-yaml', help="yaml file to output vectors to, default=None")
    parser.add_argument('-filtered_image', default=None, help="where to save the filtered output image, (default=no save file)")

    args = parser.parse_args()

    if args.columns <= 0 or args.rows <= 0:
        raise ValueError("rows and columns must be positive integers")

    return args


def base_name_no_ext(fileStr):
    return os.path.splitext(os.path.basename(fileStr))[0]


def read_filters(filenames):
    filters = []
    for filename in filenames:
        with open(filename, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            try:
                matrix = [[float(aij) for aij in row] for row in reader]
            except:
                raise ValueError("ill-formed matrix file, (not all floats) in: " + filename)
        if len(matrix) != 3 and len(matrix) != 5:
            raise ValueError("matrix must be square with a width of 3 or 5: " + filename)
        if not all(len(r) == len(matrix) for r in matrix):
            raise ValueError("matrix must be square, in: " + filename)
        f = ImageFilter.Kernel((len(matrix), len(matrix)), [x for row in matrix for x in row])
        filters.append(f)
    return filters


def apply_filters(image, filters):
    for f in filters:
        image = image.filter(f)
    return image


def bounding_box(x, y, w, h, inset=0):
    return [x + inset, y + inset, x + w - 2 * inset, y + h - 2 * inset]


def apply_index_weighting(vector, luminosity):
    return vector * np.arange(len(vector)) / luminosity


def get_weighted_vectors(image):
    image = image.convert('L')
    matrix = np.array(image.getdata())
    matrix.shape = image.size[:2]
    luminosity = matrix.sum()
    return dict(
            x=apply_index_weighting(matrix.sum(0), luminosity),
            y=apply_index_weighting(matrix.sum(1), luminosity))


def get_stats_from_wvector(w_vector, key_prefix=""):
    stat_functions = dict(mean=np.mean, stddev=np.std)
    stat_results = dict()
    for key in stat_functions:
        stat_results[key_prefix + "_" + key] = stat_functions[key](w_vector)
    return stat_results


def main(image, image_name, rows, columns, filter_list, csv_output,
        yaml_out=None, save_map_image=None, save_cell_images=False, filter_image_name=None):
    cell_w = image.size[0] / columns
    cell_h = image.size[1] / rows
    filter_name = "-".join(map(base_name_no_ext, args.filters))
    filtered_image = apply_filters(image, filter_list)
    if save_map_image:
        filtered_image.save(image_name + "-" + filter_name + ".bmp")

    if filter_image_name:
        filtered_image.save(filter_image_name)
    stats_data = []
    for i in range(columns):
        stats_data.append(list())
        for j in range(rows):
            stats_data[i].append(dict())
            bb = bounding_box(i * cell_w, j * cell_h, cell_w, cell_h)
            cell = filtered_image.crop(bb)
            if save_cell_images:
                cell_name = "{:s}-{:s}_y{0:02d}_x{0:02d}.bmp".format(image_name, filter_name, i, j)
                cell.save(cell_name)
            vectors = get_weighted_vectors(cell)
            for key in vectors:
                # union of two dict to add new keys
                stats_data[i][j].update(get_stats_from_wvector(vectors[key], key))
    if yaml_out:
        yaml_out.write(yaml_dump(stats_data))

    stat_names = stats_data[0][0].keys()
    header_names = [filter_name + "-" + stat_name for stat_name in stat_names]
    stats_writer = csv.writer(csv_output)
    stats_writer.writerow(['i', 'j'] + header_names)
    for i in range(columns):
        for j in range(rows):
            row = [i, j]
            for k in stat_names:
                row.append(stats_data[i][j][k])
            stats_writer.writerow(row)


def filename_or_file_at(file_path, default_name):
    if not file_path:
        return default_name
    elif os.path.isdir(file_path):
        return os.path.join(file_path, default_name)
    else:
        return file_path


if __name__ == "__main__":
    try:
        args = parse_args()
        image = Image.open(args.image)
        image_name = base_name_no_ext(args.image)
        filters = read_filters(args.filters)
    except Exception as e:
        print e
        sys.exit(1)

    file_name = image_name + "-" + "-".join(map(base_name_no_ext, args.filters)) + ".csv"
    csv_out = sys.stdout if not args.output else open(filename_or_file_at(args.output, file_name), "w")
    yaml_out = None if not args.yaml else open(args.yaml, "w")
    main(image, image_name, args.rows, args.columns, filters, csv_out,
        yaml_out, args.save_map_image, args.save_cell_images,
        filter_image_name=args.filtered_image)

    if csv_out != sys.stdout:
        csv_out.close()

    if yaml_out:
        yaml_out.close()
