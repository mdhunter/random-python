#!/usr/bin/env python3
"""
Scrambles an image into blocks

Copyright 2016 Mathew Hunter
"""

import argparse
import random

from PIL import Image


class Scrambler():
    """
    A class that contains functionality to scramble an image using a simple
     block shuffling method
    """

    # The number of horizontal and vertical blocks to fit into the image
    hblocks = 5
    vblocks = 5


    # Initializer
    def __init__(self, hblocks, vblocks):
        """
        Creates a new instance.

        Args:
            hblocks: the number of blocks to fit horizontally
            vblocks: the number of blocks to fit vertically
        """

        self.hblocks = hblocks
        self.vblocks = vblocks


    def scramble_image(self, source_image):
        """
        Scrambles an image.

        Args:
            source_image: an Image reference

        Returns:
            A scrambled image
        """


        # Build the random list of block ids
        block_ids = [x for x in range(0, self.vblocks * self.hblocks)]
        random.shuffle(block_ids)

        # Create an empty destination image
        dest_image = Image.new(source_image.mode, source_image.size)

        # For each block, copy the referenced block from the source image to the next
        #  block in the destination image
        current_block = 0
        for block_id in block_ids:
            self.__copy_block(source_image, block_id, dest_image, current_block)
            current_block += 1

        return dest_image


    # Calculates the pixel coordinates of the specified blocks
    def __calculate_block_coordinates(self, block_id, width, height):
        """
        Calculates pixel coordinates for a block.

        Args:
            block_id: the id of the block
            width: the width of a block
            height: the height of a block

        Returns:
            a tuple containing the upper left and lower right coordinates
        """


        # Calculate block row/column
        row = int(block_id / self.vblocks)
        column = int(block_id % self.vblocks)

        # Calculate the start and end coordinates
        start = (column * width, row * height)
        end = (start[0] + width, start[1] + height)

        return (start[0], start[1], end[0], end[1])


    # Copies a block in a source image to a destination image
    def __copy_block(self, source_image, source_block, dest_image, dest_block):
        """
        Copies a block from the source image into a block in the destination image.

        Args:
            source_image: the source image
            source_block: the id of the block in the source image to copy
            dest_image: the destination image
            dest_block: the id of the block into which to copy the source block
        """


        # Calculate block width/height
        image_size = source_image.size
        width = int(image_size[0] / self.hblocks)
        height = int(image_size[1] / self.vblocks)

        # Calculate the source and destination blocks
        source_coords = self.__calculate_block_coordinates(source_block, width, height)
        dest_coords = self.__calculate_block_coordinates(dest_block, width, height)

        # Crop a region from the source image and paste it into the destination
        region = source_image.crop(source_coords)
        dest_image.paste(region, dest_coords)



if __name__ == "__main__":

    # Parse the arguments
    parser = argparse.ArgumentParser(description="Scrambles an image into blocks")
    parser.add_argument("source_file", help="the file to scramble")
    parser.add_argument("--vblocks", nargs="?", type=int,
                        help="the number of blocks to fit vertically", default=5)
    parser.add_argument("--hblocks", nargs="?", type=int,
                        help="the number of blocks to fit horizontally", default=5)
    args = parser.parse_args()

    # Load the source image
    source_image = Image.open(args.source_file)

    # Create a Scrambler instance and scramble
    scrambler = Scrambler(args.hblocks, args.vblocks)
    dest_image = scrambler.scramble_image(source_image)

    dest_image.show()
