#!/usr/bin/python3

from openttd_types import INDUSTRY_TYPES


class TileOccupant:
    def __init__(self, parent):
        """
        Make a TileOccupant for a tile.

        :param parent: The tile where the occupant lives. The occupant sits "on" the tile.
        :type parent: TileObject.
        """

        self.parent = parent

    def parse_map_bits(self, map_name, start, end):
        """
        Parse and return the bits of the parent for a given map.

        :param map_name: The name of the map.
        :type map_name: string.

        :param start: The start of the bits string.
        :type start: integer.

        :param end: The end of the bits string. The final bit is not included.
        :type end: integer.

        :return: The value of the bits.
        :rtype: integer
        """

        return self.parent.parse_map_bits(map_name, start, end)

    def parse_all(self):
        """Parse the various properties of the TileOccupant."""
        pass


class TileOccupantRailwayTrack(TileOccupant):
    def __init__(self, parent):
        """
        Make a TileOccupantRailwayTrack for a tile.

        :param parent: The tile where the occupant lives. The occupant sits "on" the tile.
        :type parent: TileObject.
        """

        super().__init__(parent)

        self.track_type = None
        self.ground_type = None
        self.signal_type = None
        self.has_signals = None

        self.track_X = None
        self.track_Y = None
        self.track_N = None
        self.track_S = None
        self.track_W = None
        self.track_E = None

        self.is_depot = None
        self.depot_direction = None

        self.signal_0_present = None
        self.signal_1_present = None
        self.signal_2_present = None
        self.signal_3_present = None
        self.signal_01_type = None
        self.signal_23_type = None
        self.signal_23_era = None
        self.signal_23_era = None

    def parse_all(self):
        """Parse the various properties of the TileOccupant."""

        self.ship_docking_state = self.parse_map_bits(b'MAPO', 7, 8)

        self.signal_23_type = self.parse_map_bits(b'MAP2', 0, 3)
        self.signal_23_era = self.parse_map_bits(b'MAP2', 3, 4)
        self.signal_01_type = self.parse_map_bits(b'MAP2', 4, 7)
        self.signal_01_era = self.parse_map_bits(b'MAP2', 7, 8)

        self.signal_0_present = self.parse_map_bits(b'M3LO', 4, 5)
        self.signal_1_present = self.parse_map_bits(b'M3LO', 5, 6)
        self.signal_2_present = self.parse_map_bits(b'M3LO', 6, 7)
        self.signal_3_present = self.parse_map_bits(b'M3LO', 7, 8)

        self.signal_0_red = self.parse_map_bits(b'M3HI', 4, 5)
        self.signal_1_red = self.parse_map_bits(b'M3HI', 5, 6)
        self.signal_2_red = self.parse_map_bits(b'M3HI', 6, 7)
        self.signal_3_red = self.parse_map_bits(b'M3HI', 7, 8)

        self.has_signals = self.parse_map_bits(b'MAP5', 6, 7)

        self.is_depot = self.parse_map_bits(b'MAP5', 6, 8) == 3
        self.is_bridge = self.parse_map_bits(b'MAPT', 7, 8)
        self.is_tunnel = self.is_bridge and self.parse_map_bits(b'MAPT', 0, 1)
        self.entrance_direction = self.parse_map_bits(b'MAP5', 0, 2)

        if self.is_depot:
            self.depot_direction = self.parse_map_bits(b'MAP5', 0, 2)
        elif self.is_bridge:
            self.entrance_direction = self.parse_map_bits(b'MAP5', 0, 2)

        self.track_X = self.parse_map_bits(b'MAP5', 0, 1)
        self.track_Y = self.parse_map_bits(b'MAP5', 1, 2)
        self.track_N = self.parse_map_bits(b'MAP5', 2, 3)
        self.track_S = self.parse_map_bits(b'MAP5', 3, 4)
        self.track_W = self.parse_map_bits(b'MAP5', 4, 5)
        self.track_E = self.parse_map_bits(b'MAP5', 5, 6)

        self.track_type = self.parse_map_bits(b'MAP8', 0, 2)


class TileOccupantRoad(TileOccupant):
    def __init__(self, parent):
        """
        Make a TileOccupantRoad for a tile.

        :param parent: The tile where the occupant lives. The occupant sits "on" the tile.
        :type parent: TileObject.
        """

        super().__init__(parent)

        self.ground_type = None

        self.road_NW = None
        self.road_SW = None
        self.road_SE = None
        self.road_NE = None

        self.is_level_crossing = None
        self.has_signals = False

    def parse_all(self):
        """Parse the various properties of the TileOccupant."""

        self.is_level_crossing = self.parse_map_bits(b'MAP5', 6, 7)
        self.is_depot = self.parse_map_bits(b'MAP5', 6, 8) == 2

        self.road_NW = self.parse_map_bits(b'MAP5', 0, 1)
        self.road_SW = self.parse_map_bits(b'MAP5', 1, 2)
        self.road_SE = self.parse_map_bits(b'MAP5', 2, 3)
        self.road_NE = self.parse_map_bits(b'MAP5', 3, 4)

        self.tram_NW = self.parse_map_bits(b'M3LO', 0, 1)
        self.tram_SW = self.parse_map_bits(b'M3LO', 1, 2)
        self.tram_SE = self.parse_map_bits(b'M3LO', 2, 3)
        self.tram_NE = self.parse_map_bits(b'M3LO', 3, 4)

        if self.is_depot:
            self.depot_direction = self.parse_map_bits(b'MAP5', 0, 2)

        if self.is_level_crossing:
            self.level_crossing_direction = self.parse_map_bits(b'MAP5', 0, 1)
            self.track_type = self.parse_map_bits(b'MAP8', 0, 2)

        self.tram_type = self.parse_map_bits(b'MAP8', 6, 11)


class TileOccupantStation(TileOccupant):
    def __init__(self, parent):
        """
        Make a TileOccupantStation for a tile.

        :param parent: The tile where the occupant lives. The occupant sits "on" the tile.
        :type parent: TileObject.
        """

        super().__init__(parent)

        self.road_NW = None
        self.road_SW = None
        self.road_SE = None
        self.road_NE = None
        self.track_direction = None
        self.has_signals = False

    def parse_all(self):
        """Parse the various properties of the TileOccupant."""

        self.station_type = self.parse_map_bits(b'MAPE', 3, 6)
        self.station_id = self.parse_map_bits(b'MAP2', 0, 8)

        if self.station_type == 0:
            self.track_direction = self.parse_map_bits(b'MAP5', 0, 1)
            self.track_type = self.parse_map_bits(b'MAP8', 0, 2)

        elif self.station_type in [2, 3]:
            road_directions = self.parse_map_bits(b'MAP5', 0, 3)

            self.road_NW = False
            self.road_SW = False
            self.road_SE = False
            self.road_NE = False

            if road_directions == 0:
                self.road_NE = True
            if road_directions == 1:
                self.road_SE = True
            if road_directions == 2:
                self.road_SW = True
            if road_directions == 3:
                self.road_NW = True
            if road_directions == 4:
                self.road_NE = True
                self.road_SW = True
            if road_directions == 5:
                self.road_NW = True
                self.road_SE = True

            self.tram_NW = self.parse_map_bits(b'M3LO', 0, 1)
            self.tram_SW = self.parse_map_bits(b'M3LO', 1, 2)
            self.tram_SE = self.parse_map_bits(b'M3LO', 2, 3)
            self.tram_NE = self.parse_map_bits(b'M3LO', 3, 4)

        if self.station_type == 7:
            self.track_direction = self.parse_map_bits(b'MAP5', 0, 1)
            self.track_type = self.parse_map_bits(b'MAP8', 0, 2)

        self.tram_type = self.parse_map_bits(b'MAP8', 6, 11)


class TileOccupantIndustry(TileOccupant):
    def __init__(self, parent):
        """
        Make a TileOccupantIndustry for a tile.

        :param parent: The tile where the occupant lives. The occupant sits "on" the tile.
        :type parent: TileObject.
        """

        super().__init__(parent)

        self.industry_type = None

    def parse_all(self):
        """Parse the various properties of the TileOccupant."""

        self.industry_type = INDUSTRY_TYPES[self.parse_map_bits(b'MAP5', 0, 8)]
        self.industry_id = self.parse_map_bits(b'MAP2', 0, 8)


class TileOccupantBridgeOrTunnel(TileOccupant):
    def __init__(self, parent):
        """
        Make a TileOccupantBridgeOrTunnel for a tile.

        :param parent: The tile where the occupant lives. The occupant sits "on" the tile.
        :type parent: TileObject.
        """

        super().__init__(parent)

        self.ground_type = None
        self.entrance_direction = None
        self.payload_kind = None
        self.is_bridge = self.parse_map_bits(b'MAP5', 7, 8)
        self.has_signals = False

    def parse_all(self):
        """Parse the various properties of the TileOccupant."""

        self.entrance_direction = self.parse_map_bits(b'MAP5', 0, 2)
        self.payload_kind = self.parse_map_bits(b'MAP5', 2, 4)
        self.is_bridge = self.parse_map_bits(b'MAP5', 7, 8)
        self.is_tunnel = not self.is_bridge

        if self.payload_kind == 0:
            self.track_type = self.parse_map_bits(b'MAP8', 0, 2)

        self.tram_type = self.parse_map_bits(b'MAP8', 6, 11)
