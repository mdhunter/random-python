#!/usr/bin/env python3

# Reads an image and categorizes it for color.
#
# Copyright 2016 Mathew Hunter

import argparse
import colorsys
import operator
from PIL import Image


# A dictionary that checks stored ranges for a key
# Taken from: http://stackoverflow.com/questions/13464143/use-a-range-as-a-dictionary-key-in-python-what-option-do-i-have
class RangeDictionary(dict):
    def __getitem__(self, key):
        for r in self.keys():
            if key in r:
                return super().__getitem__(r)
        return super().__getitem__(key)


# The collection of color names and their degree positions
# Taken from: http://stackoverflow.com/questions/21737613/image-of-hsv-color-wheel-for-opencv
color_names_and_degrees = {
    "mid red": 0,
    "warm red": 15,
    "orange": 30,
    "warm yellow": 45,
    "mid yellow": 60,
    "cool yellow": 75,
    "yellow green": 90,
    "warm green": 105,
    "mid green": 120,
    "cool green": 135,
    "green cyan": 150,
    "warm cyan": 165,
    "mid cyan": 180,
    "cool cyan": 195,
    "blue cyan": 210,
    "cool blue": 225,
    "mid blue": 240,
    "warm blue": 255,
    "violet": 270,
    "cool magenta": 285,
    "mid magenta": 300,
    "warm magenta": 315,
    "red magenta": 330,
    "cool red": 345
}

# A dictionary that maps the degree ranges for a color to its name
color_names_by_range = RangeDictionary({})


# Converts an RGB color to a name
def __convert_rgb_to_color_name(r, g, b):

    # Convert to HSV for easier identification
    (h, s, v) = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    c_h = int(h * 360)
    c_s = int(s * 100)
    c_v = int(v * 100)

    if c_v <= 10:
        return "black"
    if c_s <= 10 and c_v >= 90:
        return "white"

    return color_names_by_range[c_h]


# Scans the specified image file for colors and builds a collection
def scan_image_for_colors(image_filename):

    # Initialize the dictionary for color names by range
    for name, degrees in color_names_and_degrees.items():
        low = degrees - 7
        high = degrees + 8
        if low < 0:
            color_names_by_range[range(low + 360, 360)] = name
            color_names_by_range[range(0, high)] = name
        elif high > 360:
            color_names_by_range[range(low, 360)] = name
            color_names_by_range[range(0, high - 360)] = name
        else:
            color_names_by_range[range(low, high)] = name

    # Open and analyze the image
    colors = {}
    with Image.open(image_filename) as image:
        rgb_image = image.convert("RGB")
        for (r, g, b) in image.getdata():
            color_name = __convert_rgb_to_color_name(r, g, b)
            if color_name not in colors:
                colors[color_name] = 0
            colors[color_name] += 1

    # Sort by frequency
    sorted_colors = sorted(colors.items(), key=operator.itemgetter(1), reverse=True)

    # Output
    total = 0
    for (name, occurrences) in sorted_colors:
        total += occurrences
        print("{0:15s}: {1}".format(name, occurrences))
    print("{0:15s}: {1}".format("Total", total))


if __name__ == "__main__":

    # Parse the arguments
    parser = argparse.ArgumentParser(description="Scans an image and categorizes it for color")
    parser.add_argument("source_file", help="the file to scan")
    args = parser.parse_args()

    # Scan the image
    scan_image_for_colors(args.source_file)
