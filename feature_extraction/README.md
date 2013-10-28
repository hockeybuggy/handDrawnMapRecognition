# Limitations

The scripts only look at black or white (they use a threshold to determine that).
They are sensitive to the colour of the symbol. Changing to a black outline on
a white background will not give the same results as a white background on black.
after transforming the image, parts that were not within the original image are set to black in PIL.
In PIL it is difficult to tell it what colour of pixel to use instead, it may be easier to
have an alpha channel, transform the image, and then paste it into a new image with a white background.

# TODO

* transform.py needs to draw into a white canvas.
* Convert image to grey scale only when necessary


# Testing

There is a gimp image file with modifications applied to a base layer for use in testing.
The PIL version I'm using only seems to work with png files made by gimp, PIL doesn't like
the bmp or jpeg format that gimp produces.


# Scripts

affine.py
:   A library for combining affine transform matrices

class_feature_plot.py
:   not yet useful.

feature_extraction.py
:   Creates a csv with a bunch of statistics applied after the filter.

filters
:   CSV files to use with feature_extraction.py

pixel_distribution.py
:   Another CSV which collects stats to use with transform.py

test_images
:   Images for testing transform.py and pixel_distribution.py

transform.py
:   create a new image translation, scaling, and rotating an image.

vec_plot.py
:   not useful yet.
