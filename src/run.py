#!/usr/bin/python3

import argparse
import logging
import os
import random

from surveyor import Surveyor


def main():
    """
    Parse a save file and save images to disk.
    """

    random.seed(123)

    default_config_path = "config/martin.json"
    default_tile_size = 51

    argparser = argparse.ArgumentParser(description='Make a map of an OpenTTD save.')
    argparser.add_argument(
        "-i", "--input-path",
        help="Path to the save file.",
        default="example_saves/tiny.sav",
        type=str)
    argparser.add_argument(
        "-o", "--output-dir",
        help="Path to the outptut directory.",
        default="example_images",
        type=str)
    argparser.add_argument(
        "-f", "--output-filename",
        help="Name of the output file. It's best to leave this blank and let the program choose for you.",
        default="",
        type=str)
    argparser.add_argument(
        "-c", "--config",
        help="Path to the config file.",
        default=default_config_path,
        type=str)
    argparser.add_argument(
        "-m", "--mode",
        help="Image mode, one of: ['svg', 'png'].",
        default="PNG",
        type=str)
    argparser.add_argument(
        "-s", "--tile_size",
        help="Size of the tile. Should be an odd integer. May be ignored for very large maps.",
        default=default_tile_size,
        type=int)
    argparser.add_argument(
        "-v", "--verbose",
        help="If set, use verbose logging.",
        default=False,
        action="store_true")
    argparser.add_argument(
        "-p", "--progress-bar",
        help="If set, show progress bar for time consuming methods.",
        default=False,
        action="store_true")
    argparser.add_argument(
        "-d", "--dark-mode",
        help="If set, use dark mode. This is ignored if config is set to anything other than 'config/main.json'.",
        default=False,
        action="store_true")
    args = argparser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    tile_size = int(args.tile_size)
    if tile_size % 2 == 0:
        tile_size = tile_size - 1
    tile_size = max(tile_size, 5)
    if tile_size == default_tile_size:
        tile_size = None

    if args.output_filename:
        output_filename = args.output_filename
    else:
        save_filename = args.input_path.split("/")[-1]
        output_filename = ".".join(save_filename.split(".")[:-1])
        output_filename = f"{output_filename}.{args.mode}"
        output_filename = output_filename.lower()

    image_mode = args.mode.upper()
    save_file_path = args.input_path
    config_file_path = args.config
    output_file_path = os.path.join(args.output_dir, output_filename)
    show_progress_bar = args.progress_bar

    if config_file_path == default_config_path and args.dark_mode:
        config_file_path = 'config/dark_mode.json'

    print("Working with the following settings:")
    print(f"   save_file_path: {save_file_path}")
    print(f" output_file_path: {output_file_path}")
    print(f" config_file_path: {config_file_path}")
    print(f"       image_mode: {image_mode}")
    print(f"        tile_size: {tile_size}")
    print(f"          verbose: {args.verbose}")
    print(f"show_progress_bar: {show_progress_bar}")
    print(f"        dark_mode: {args.dark_mode}")

    surveyor = Surveyor(save_file_path, show_progress_bar=show_progress_bar)
    surveyor.ingest_data()
    surveyor.load_settings(config_file_path, tile_size)
    surveyor.save_image(output_file_path, image_mode)


if __name__ == '__main__':
    main()
