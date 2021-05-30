#!/usr/bin/python3

from tile_occupant import (
    TileOccupant,
    TileOccupantRailwayTrack,
    TileOccupantRoad,
    TileOccupantStation,
    TileOccupantIndustry,
    TileOccupantBridgeOrTunnel
)

POWERS_OF_TWO = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]


class TileObject:
    def __init__(self, row, col):
        """
        Make a new TileObject.

        :param row: The row of the tile.
        :type row: integer.

        :param col: The column of the tile.
        :type col: integer.
        """

        self.row = row
        self.col = col
        self.map_names = []
        self.map_bytes = []
        self.map_indices = {}

        self.kind = 'NOT_SET'
        self.zone = 'NOT_SET'
        self.bridge = 'NOT_SET'
        self.height = 0
        self.occupant = None

    def set_map_bytes(self, map_name, map_bytes):
        """
        Set the bytes for a given map.

        :param map_name: The name of the map.
        :type map_name: string.

        :param map_bytes: The bytes from the map for this tile.
        :type map_bytes: list of bytes.
        """

        value = 0
        shift = 0
        map_bytes = bytearray(map_bytes)
        map_bytes.reverse()
        for byte in map_bytes:
            value += int(byte << shift)
            shift += 8

        self.map_indices[map_name] = len(self.map_names)
        self.map_bytes.append(value)
        self.map_names.append(map_name)

    def get_bits_values(self, map_index, start, end):
        """
        Parse and return the bits for a given map.

        :param map_index: The index of the map.
        :type map_index: integer.

        :param start: The start of the bits string.
        :type start: integer.

        :param end: The end of the bits string. The final bit is not included.
        :type end: integer.

        :return: The value of the bits.
        :rtype: integer

        Note that the MAPS are generally not aligned to the map indices. For example, MAP2 is at index 3.
        To return the value for the 3rd, 4th, 5th bits of MAP2, call self.get_bits_values(3, 3, 6).
        """

        value = self.map_bytes[map_index]
        value = value % POWERS_OF_TWO[end]
        value = value // POWERS_OF_TWO[start]
        return value

    def parse_map_bits(self, map_name, start, end):
        """
        Parse and return the bits for a given map.

        :param map_name: The name of the map.
        :type map_name: string

        :param start: The start of the bits string.
        :type start: integer.

        :param end: The end of the bits string. The final bit is not included.
        :type end: integer.

        :return: The value of the bits.
        :rtype: integer

        Note that the MAPS are generally not aligned to the map indices. For example, MAP2 is at index 3.
        To return the value for the 3rd, 4th, 5th bits of MAP2, call self.get_bits_values(3, 3, 6).
        """

        map_index = self.map_indices[map_name]
        return self.get_bits_values(map_index, start, end)

    def parse_common(self):
        """Set the common parameters from the bits."""

        self.zone = self.parse_map_bits(b'MAPT', 0, 2)
        self.bridge = self.parse_map_bits(b'MAPT', 2, 4)
        self.kind = self.parse_map_bits(b'MAPT', 4, 8)
        self.height = self.parse_map_bits(b'MAPH', 0, 8)
        self.owner = self.parse_map_bits(b'MAPO', 0, 4)
        self.owner_tram = self.parse_map_bits(b'M3LO', 4, 8)
        self.over_bridge_owner = None

    def parse_all(self):
        """Set everything for the tile from the bits."""

        self.parse_common()
        self.occupant = TileOccupant(self)

        if self.kind == 1:
            self.occupant = TileOccupantRailwayTrack(self)
        if self.kind == 2:
            self.occupant = TileOccupantRoad(self)
        if self.kind == 5:
            self.occupant = TileOccupantStation(self)
        if self.kind == 8:
            self.occupant = TileOccupantIndustry(self)
        if self.kind == 9:
            self.occupant = TileOccupantBridgeOrTunnel(self)

        self.occupant.parse_all()
