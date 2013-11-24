# Limitations

The scripts only look at black or white (they use a threshold to determine that).
They are sensitive to the colour of the symbol. Changing to a black outline on
a white background will not give the same results as a white background on black.
after transforming the image, parts that were not within the original image are set to black in PIL.
In PIL it is difficult to tell it what colour of pixel to use instead, it may be easier to
have an alpha channel, transform the image, and then paste it into a new image with a white background.


# Testing

There is a gimp image file with modifications applied to a base layer for use in testing.
The PIL version I'm using only seems to work with png files made by gimp, PIL doesn't like
the bmp or jpeg format that gimp produces.


# Scripts

add_map_name.sh

affine.py
:   A library for combining affine transform matrices

align_images.py

black_and_white.py
:   converts an image to black and white with optional threshold value

class_feature_plot.py
:   not yet useful.

compare_images.py
:   computes a squared error for a pixel-pixel comparison

crop.py

csv_join.py

dims.py

extract_features_from_image.py

feature_extraction.py
:   Creates a csv with a bunch of statistics applied after the filter.

gold_comparison.py

gold_means.yml

greyscale.py
:   converts and image to greyscale

image_replace.py
:   uses fuzzy filter to find and replace a colour in an image

mean_cell_images.py

mean_images.py

pivot_csv_map.py

pixel_distribution.py

proximity_statistics.py
:   Another CSV which collects stats to use with transform.py

run_j48.sh

show_grid.py

show_means.py

transform.py
:   create a new image translation, scaling, and rotating an image.

vec_plot.py
