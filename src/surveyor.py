import datetime
import logging
import lzma

from alive_progress import alive_bar

from tile import TileObject
from tile_grid import TileGrid
from cairo_painter import CairoPainter


class Surveyor:
    def __init__(self, file_path, compression='lzma', logging_level=logging.INFO, show_progress_bar=False):
        """
        Create a SaveFileParser.

        :param file_path: The path to the save file.
        :type file_path: string.

        :param compression: The type of compression to use. Defaults to 'lzma'.
        :type compression: string.

        :param logging_level: The level of logging. Defaults to logging.INFO.
        :type logging_level: logging.LEVEL.

        :param show_progress_bar: If true, use alive_bar on expensive functions. Defaults to False.
        :type show_progress_bar: Boolean.
        """

        self.logger = logging.getLogger("Surveyor")
        self.file_path = file_path
        self.painter = CairoPainter(self)
        self.show_progress_bar = show_progress_bar

        with open(file_path, 'rb') as file_in_handle:
            self.raw_source = file_in_handle.read()

        self.file_type = self.raw_source[0:4]
        self.file_version = int.from_bytes(self.raw_source[5:8], "little")
        self.log_message(f"Save file version: {self.file_version}")

        if compression == "lzma":
            self.data = lzma.decompress(self.raw_source[8:])
        else:
            self.data = self.raw_source[8:]

    def log_message(self, message, level=logging.INFO):
        """
        Send a message to the logger.

        :param message: The message to log.
        :type message: string.

        :param level: The level of the message. Default of logging.INFO.
        :type level: logging level.
        """

        message_with_time = f"[{datetime.datetime.now()}]  {message}"

        if level == logging.ERROR:
            self.logger.error(message_with_time)
        elif level == logging.WARNING:
            self.logger.warning(message_with_time)
        elif level == logging.INFO:
            self.logger.info(message_with_time)
        elif level == logging.DEBUG:
            self.logger.debug(message_with_time)

    def get_int(self, offset, n_bytes=1):
        """
        Return the int value from self.data, based on the offset and n_bytes.

        :param offset: The offset of the data, where the reading should start.
        :type offset: integer.

        :param n_bytes: The number of bytes to parse. Defaults to 1.
        :type n_bytes: integer.

        :return: The value of the bytes.
        :rtype: integer
        """

        return int.from_bytes(self.data[offset:offset + n_bytes], 'big')

    def parse_size(self):
        """Parse the size of the maps."""

        MAPS_start = self.data.find(b"MAPS")
        self.ncols = self.get_int(MAPS_start + 8, 4)
        self.nrows = self.get_int(MAPS_start + 12, 4)
        self.log_message(f"Map size: {self.nrows} x {self.ncols}")

    def make_tiles(self):
        """Make the blank tiles."""

        n_tiles = (self.nrows) * (self.ncols)
        self.log_message("Making tiles...")
        self.tiles = [TileObject(i // self.ncols, i % self.ncols) for i in range(n_tiles)]
        self.log_message("Done!")

    def set_map_bytes(self):
        """Populate the tiles from the parsed maps."""

        maps_info = {
            b'MAPT': [1, 8],
            b'MAPH': [1, 8],
            b'MAPO': [1, 8],
            b'MAP2': [2, 8],
            b'M3LO': [1, 8],
            b'M3HI': [1, 8],
            b'MAP5': [1, 8],
            b'MAPE': [1, 8],
            b'MAP7': [1, 8],
            b'MAP8': [2, 8]
        }

        for map_name in maps_info:
            self.log_message(f"Reading {map_name}...")
            start = self.data.find(map_name)
            m = maps_info[map_name][0]
            n_tiles = len(self.tiles)
            offset = start + maps_info[map_name][1]

            tbs = self.data[offset:offset + self.ncols * self.nrows * m]
            [self.tiles[i].set_map_bytes(map_name, tbs[i * m:(i + 1) * m]) for i in range(n_tiles)]

        self.log_message("Parsing tile bits...")

        if self.show_progress_bar:
            with alive_bar(len(self.tiles)) as abar:
                for tile in self.tiles:
                    tile.parse_all()
                    abar()
        else:
            for tile in self.tiles:
                tile.parse_all()
        self.log_message("All done!")

        heights = [tile.height for tile in self.tiles]
        self.min_height = min(heights)
        self.max_height = max(heights)
        self.log_message(f"Min, max map height: {self.min_height}, {self.max_height}")

    def make_tile_grid(self):
        """Make the grid of tiles."""

        self.tile_grid = TileGrid(self.nrows, self.ncols, self.tiles)

    def ingest_data(self):
        """Parse the size of the map, make the tiles, and set the tiles data."""

        self.parse_size()
        self.make_tiles()
        self.set_map_bytes()
        self.make_tile_grid()

    def load_settings(self, settings_file_path, tile_size):
        """
        Load settings from file.

        :param settings_file_path: The path to the settings file.
        :type settings_file_path: string.

        :param tile_size: The tile size to use.
        :type tile_size: integer.
        """

        self.painter.load_settings(settings_file_path, tile_size)

    def save_image(self, image_file_path, filetype="PNG", settings_file_path=None):
        """
        Make a nice image and save it to file.

        :param image_file_path: The path to the output file. It should not include an extension.
        :type image_file_path: string.

        :param filetype: The type of file to save to. Supports PNG and SVG. Defaults to PNG.
        :type filetype: string.

        :param settings_file_path: The path to the settings file. Defaults to None.
        :type settings_file_path: string.
        """

        if settings_file_path:
            self.load_settings(settings_file_path)

        self.painter.save_image(image_file_path, filetype=filetype)
