import json
import math
import random

from alive_progress import alive_bar
import cairo


def do_nothing():
    """Do nothing. A dummy function to use in place of alive_bar."""
    pass


class CairoPainter:
    """
    A class to interface with the Cairo library to draw the map for a given save file.
    """

    def __init__(self, parent):
        """
        :param parent: The SaveFileParser used to get useful information.
        :type parent: SaveFileParser.
        """

        self.parent = parent

        self.player_colors = [
            (200, 0, 0),
            (0, 0, 200),
            (100, 0, 0),
            (0, 0, 100),
            (0, 200, 200),
            (200, 0, 200),
            (200, 200, 0),
            (0, 100, 100),
            (100, 0, 100),
            (100, 100, 0),
            (200, 200, 200),
            (100, 100, 100),
            (50, 50, 50),
            (0, 0, 0),
            (0, 200, 0),
            (0, 100, 0),
        ]

    def log_message(self, message):
        """
        Send a message to the logger.

        :param message: The message to log.
        :type message: string.
        """

        self.parent.log_message(message)

    def get_progress_bar(self, tiles):
        """
        Return a callback for a progress bar.

        :param tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.
        """

        if self.parent.show_progress_bar:
            return alive_bar(len(tiles))
        return do_nothing

    def load_settings(self, file_path, tile_size):
        """
        Update the settings, given a config file path.

        :param file_path: The path to the config file.
        :type file_path: string.

        :param tile_size: Override for tile size.
        :type tile_size: integer.
        """

        with open(file_path) as file_handle:
            settings = json.load(file_handle)

        self.ds = settings.get("ds", 25)
        self.ss = 2 * self.ds

        self.ocean_noise = settings.get("ocean_noise", 50)

        self.road_tile_rgb = settings.get("road_tile_rgb", (100, 100, 100))
        self.rail_rgb = settings.get("rail_rgb", (255, 255, 255))
        self.road_rgb = settings.get("road_rgb", (255, 255, 255))
        self.tram_rgb = settings.get("tram_rgb", (255, 255, 255))

        self.railway_rgb = settings.get("railway_rgb", (255, 255, 255))
        self.electrified_railway_rgb = settings.get("electrified_railway_rgb", (200, 200, 200))
        self.monorail_rgb = settings.get("monorail_rgb", (150, 150, 150))
        self.maglev_rgb = settings.get("maglev_rgb", (100, 100, 100))

        self.town_building_rgb = settings.get("town_building_rgb", (255, 255, 255))
        self.industry_rgb = settings.get("industry_rgb", (255, 165, 0))
        self.industry_edge_rgb = settings.get("industry_edge_rgb", (0, 0, 0))
        self.torb_rgb = settings.get("torb_rgb", (150, 150, 150))
        self.objects_rgb = settings.get("objects_rgb", (150, 150, 150))
        self.torb_edge_rgb = settings.get("torb_edge_rgb", (0, 100, 100))

        self.station_rgb = settings.get("station_rgb", (255, 0, 255))
        self.rail_station_rgb = settings.get("rail_station_rgb", (255, 0, 255))
        self.bus_station_rgb = settings.get("bus_station_rgb", (255, 0, 255))
        self.truck_station_rgb = settings.get("truck_station_rgb", (255, 0, 255))
        self.airport_rgb = settings.get("airport_rgb", (255, 255, 0))
        self.seaport_rgb = settings.get("seaport_rgb", (0, 255, 255))
        self.heliport_rgb = settings.get("heliport_rgb", (255, 255, 0))

        self.rail_depot_rgb = settings.get("rail_depot_rgb", (0, 100, 100))
        self.road_depot_rgb = settings.get("road_depot_rgb", (0, 100, 100))
        self.ship_depot_rgb = settings.get("ship_depot_rgb", (0, 100, 100))

        self.screen_mode = settings.get("screen_mode", "normal")
        self.player_colors = settings.get("player_colors", self.player_colors)

        if tile_size:
            self.ss = tile_size
            self.ds = (tile_size - 1) // 2

        # Thicknesses of various elements.
        self.rail_width = self.ds / 3
        self.road_width = self.ds / 2
        self.tram_width = self.ds / 5
        self.bridge_edge_width = self.ss / 10
        self.edge_width = int(0.1 * self.ss)
        if self.edge_width % 2 == 0:
            self.edge_width += 1

    def set_rgb(self, rgb):
        """
        Set the RGB for the context.

        :param rgb: The fill color, expressed as a tuple in the range (0-255, 0-255, 0-255).
        :type rgb: (integer, integer, integer).
        """

        ctx = self.context
        (rgb_r, rgb_g, rgb_b) = rgb
        ctx.set_source_rgb(rgb_r / 255, rgb_g / 255, rgb_b / 255)

    def set_rgba(self, rgba):
        """
        Set the RGBA for the context.

        :param rgba: The fill color, expressed as a tuple in the range (0-255, 0-255, 0-255, 0-1).
        :type rgba: (integer, integer, integer, integer).
        """

        ctx = self.context
        (rgba_r, rgba_g, rgba_b, rgba_a) = rgba
        ctx.set_source_rgba(rgba_r / 255, rgba_g / 255, rgba_b / 255, rgba_a)

    def draw_line(self, x1, y1, x2, y2, rgb, width, round_cap=True):
        """
        Draw a line on the context.

        :param x1: The x coordinate of the top left corner.
        :type x1: float

        :param y1: The y coordinate of the top left corner.
        :type y1: float

        :param x2: The x coordinate of the bottom right corner.
        :type x2: float

        :param y2: The y coordinate of the bottom right  corner.
        :type y2: float

        :param rgb: The fill color, expressed as a tuple in the range (0-255, 0-255, 0-255).
        :type rgb: (integer, integer, integer).

        :param width: The width of the line.
        :type width: float

        :param round_cap: If True, set the line cap to round. Defaults to False.
        :type round_cap: Boolean
        """

        ctx = self.context
        ctx.save()
        self.set_rgb(rgb)
        ctx.set_line_width(width)

        if round_cap:
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        ctx.restore()

    def draw_rectangle(self, x, y, w, h, rgb_fill, rgb_stroke=None):
        """
        Fill a rectangle on the context.

        :param x: The x coordinate of the top left corner.
        :type x: float

        :param y: The y coordinate of the top left corner.
        :type y: float

        :param w: The width of the rectangle.
        :type w: float

        :param h: The height of the rectangle.
        :type h: float

        :param rgb_fill: The fill color, expressed as a tuple in the range (0-255, 0-255, 0-255).
        :type rgb_fill: (integer, integer, integer).

        :param rgb_stroke: The stroke color, expressed as a tuple in the range (0-255, 0-255, 0-255).
        :type rgb_stroke: (integer, integer, integer).
        """

        ctx = self.context
        ctx.save()

        self.set_rgb(rgb_fill)
        ctx.rectangle(x, y, w, h)
        ctx.fill()

        if rgb_stroke is not None:
            self.set_rgb(rgb_stroke)
            ctx.rectangle(x, y, w, h)
            ctx.stroke()

        ctx.restore()

    def draw_rectangle_rgba(self, x, y, w, h, rgba):
        """
        Fill a rectangle on the context.

        :param x: The x coordinate of the top left corner.
        :type x: float

        :param y: The y coordinate of the top left corner.
        :type y: float

        :param w: The width of the rectangle.
        :type w: float

        :param h: The height of the rectangle.
        :type h: float

        :param rgba: The fill color, expressed as a tuple in the range (0-255, 0-255, 0-255, 0-1).
        :type rgba: (integer, integer, integer, integer).
        """

        ctx = self.context
        ctx.save()
        self.set_rgba(rgba)
        ctx.rectangle(x, y, w, h)
        ctx.fill()
        ctx.restore()

    def cxy_from_rc(self, row, col):
        """
        Get the centre of a tile, given its row and column.

        :param row: The row of the tile.
        :type row: integer

        :param col: The column of the tile.
        :type col: integer

        :return: The coordinates of the centre of the tile, a tuple of floats.
        :rtype: (float, float)
        """

        x = (self.parent.ncols - col - 1.0 - 0.5) * self.ss
        y = (row - 0.5) * self.ss
        cx = int(x + 0.5 * self.ss)
        cy = int(y + 0.5 * self.ss)
        return cx, cy

    def xy_from_tile(self, tile):
        """
        Get the top left corner of a tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :return: The coordinates of the centre of the tile, a tuple of floats.
        :rtype: (float, float)
        """

        x = int((self.parent.ncols - tile.col - 1 - 0.5) * self.ss)
        y = int((tile.row - 0.5) * self.ss)
        return x, y

    def cxy_from_tile(self, tile):
        """
        Get the centre of a tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :return: The coordinates of the centre of the tile, a tuple of floats.
        :rtype: (float, float)
        """

        return self.cxy_from_rc(tile.row, tile.col)

    def transform_to_tile(self, tile, rotation):
        """
        Transform the context to a given tile, with a rotation.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the triangle, in the range 0, 3.
        :type rotation: integer
        """

        ctx = self.context
        ctx.save()

        cx, cy = self.cxy_from_tile(tile)

        ctx.translate(cx + 0.5, cy + 0.5)
        ctx.rotate(0.5 * math.pi * rotation)

    def end_transform_to_tile(self):
        """Restore the context. This should be called after transform_to_tile."""

        self.context.restore()

    def draw_square(self, tile, rgb_fill, rgb_stroke=None):
        """
        Draw a square for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rgb: The fill color, expressed as a tuple in the range (0-255, 0-255, 0-255).
        :type rgb: (integer, integer, integer).

        :param rgb_stroke: The stroke color, expressed as a tuple in the range (0-255, 0-255, 0-255). Default is None.
        :type rgb_stroke: (integer, integer, integer).
        """

        x, y = self.xy_from_tile(tile)
        w = self.ss
        h = self.ss

        if rgb_stroke is None:
            rgb_stroke = rgb_fill

        self.draw_rectangle(x, y, w, h, rgb_fill, rgb_stroke=rgb_stroke)

    def draw_rail_background(self, tile):
        """
        Draw the background for a given tile that contains railway track.

        :param tile: The tile to consider.
        :type tile: TileObject
        """

        rgb = self.player_colors[tile.owner]
        self.draw_square(tile, rgb)

    def draw_rail_line(self, x1, y1, x2, y2, track_type, line_mode="outer", round_cap=False, owner=0):
        """
        Draw a line for a railway track.

        :param x1: The x coordinate of the start of the line.
        :type x1: float

        :param y1: The y coordinate of the start of the line.
        :type y1: float

        :param x2: The x coordinate of the end of the line.
        :type x2: float

        :param y2: The y coordinate of the end of the line.
        :type y2: float

        :param track_type: The type of track (railway, electrified railway, monorail, maglev).
        :type track_type: integer

        :param line_mode: Whether to draw the outer or inner line for the payload. Default is False.
        :type line_mode: Boolean

        :param round_cap: If True, set the line cap to round. Defaults to False.
        :type round_cap: Boolean

        :param owner: The index of the owner. Defaults to 0.
        :type owner: Integer
        """

        do_draw_inner = line_mode in ["inner", "both"]
        do_draw_outer = line_mode in ["outer", "both"]
        if do_draw_outer:
            fills = [
                self.railway_rgb,
                self.electrified_railway_rgb,
                self.monorail_rgb,
                self.maglev_rgb
            ]
            self.draw_line(
                x1, y1, x2, y2, fills[track_type], 2.5 * self.rail_width, round_cap
            )

        if do_draw_inner:
            rgb = self.player_colors[owner]
            self.draw_line(x1, y1, x2, y2, rgb, self.rail_width, round_cap)

    def draw_rail_XY(self, tile, rotation, line_mode="outer"):
        """
        Draw a railway track in the X or Y direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the railway track, in the range 0, 1.
        :type rotation: integer

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean, Default is False.
        """

        track_type = tile.occupant.track_type

        self.transform_to_tile(tile, rotation)

        self.draw_rail_line(
            -0.5 * self.ss, 0, 0.5 * self.ss, 0, track_type,
            line_mode=line_mode, round_cap=False, owner=tile.owner
        )

        self.end_transform_to_tile()

    def draw_rail_NSEW(self, tile, rotation, line_mode="outer"):
        """
        Draw a railway track in the N, S, E or W direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the railway track, in the range 0, 3.
        :type rotation: integer

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        track_type = tile.occupant.track_type

        self.transform_to_tile(tile, rotation)

        self.draw_rail_line(
            0, 0.5 * self.ss, 0.5 * self.ss, 0, track_type,
            line_mode=line_mode, round_cap=True, owner=tile.owner
        )

        self.end_transform_to_tile()

    def draw_rail_X(self, tile, line_mode="outer"):
        """
        Draw a railway track in the X direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        self.draw_rail_XY(tile, 0, line_mode=line_mode)

    def draw_rail_Y(self, tile, line_mode="outer"):
        """
        Draw a railway track in the Y direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        self.draw_rail_XY(tile, 1, line_mode=line_mode)

    def draw_rail_N(self, tile, line_mode="outer"):
        """
        Draw a railway track in the N direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        self.draw_rail_NSEW(tile, 3, line_mode=line_mode)

    def draw_rail_W(self, tile, line_mode="outer"):
        """
        Draw a railway track in the W direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        self.draw_rail_NSEW(tile, 2, line_mode=line_mode)

    def draw_rail_S(self, tile, line_mode="outer"):
        """
        Draw a railway track in the S direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        self.draw_rail_NSEW(tile, 1, line_mode=line_mode)

    def draw_rail_E(self, tile, line_mode="outer"):
        """
        Draw a railway track in the E direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        self.draw_rail_NSEW(tile, 0, line_mode=line_mode)

    def draw_rail_depot(self, tile, rotation):
        """
        Draw a railway depot for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the depot entrance, in the range 0, 3.
        :type rotation: integer
        """

        track_type = tile.occupant.track_type
        ss = self.ss

        self.transform_to_tile(tile, rotation)
        self.draw_rail_line(
            -0.2 * ss, 0, 0.5 * ss, 0, track_type,
            line_mode="both", round_cap=False, owner=tile.owner
        )
        self.draw_line(-0.2 * ss, 0.3 * ss, -0.2 * ss, -0.3 * ss, self.rail_rgb, 0.2 * ss)
        self.end_transform_to_tile()

    def draw_signal(self, cx, cy, fill_rgb, stroke_rgb):
        """
        Draw a railway signal for a given tile.

        :param cx: The x position of the signal.
        :type cx: Float

        :param cy: The y position of the signal.
        :type cy: Float

        :param rgb: The fill color, expressed as a tuple in the range (0-255, 0-255, 0-255).
        :type rgb: (integer, integer, integer).

        :param rgb_stroke: The stroke color, expressed as a tuple in the range (0-255, 0-255, 0-255). Default is None.
        :type rgb_stroke: (integer, integer, integer).
        """

        ctx = self.context
        r = 0.1 * self.ss
        lw = 0.025 * self.ss

        self.set_rgb(fill_rgb)
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.fill()

        self.set_rgb(stroke_rgb)
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.set_line_width(lw)
        ctx.stroke()

    def draw_rail_signals_tile(self, tile, rotation):
        """
        Draw a railway signals for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the depot entrance, in the range 0, 3.
        :type rotation: integer
        """

        ss = self.ss

        self.transform_to_tile(tile, rotation)

        rail = tile.occupant

        fill_rgb = (0, 255, 0)
        stroke_rgb = (0, 0, 0)
        d1 = 0.1 * ss
        d2 = 0.2 * ss
        d3 = 0.4 * ss

        if rail.has_signals:
            if rail.track_X:
                if rail.signal_2_present:
                    self.draw_signal(d3, -d2, fill_rgb, stroke_rgb)
                if rail.signal_3_present:
                    self.draw_signal(-d3, d2, fill_rgb, stroke_rgb)

            if rail.track_Y:
                if rail.signal_2_present:
                    self.draw_signal(d2, d3, fill_rgb, stroke_rgb)
                if rail.signal_3_present:
                    self.draw_signal(-d2, -d3, fill_rgb, stroke_rgb)

            if rail.track_W:
                if rail.signal_2_present:
                    self.draw_signal(-d3, -d3, fill_rgb, stroke_rgb)
                if rail.signal_3_present:
                    self.draw_signal(-d1, -d1, fill_rgb, stroke_rgb)

            if rail.track_E:
                if rail.signal_0_present:
                    self.draw_signal(d1, d1, fill_rgb, stroke_rgb)
                if rail.signal_1_present:
                    self.draw_signal(d3, d3, fill_rgb, stroke_rgb)

            if rail.track_N:
                if rail.signal_2_present:
                    self.draw_signal(d3, -d3, fill_rgb, stroke_rgb)
                if rail.signal_3_present:
                    self.draw_signal(d1, -d1, fill_rgb, stroke_rgb)

            if rail.track_S:
                if rail.signal_0_present:
                    self.draw_signal(-0.1 * ss, 0.1 * ss, fill_rgb, stroke_rgb)
                if rail.signal_1_present:
                    self.draw_signal(-0.4 * ss, 0.4 * ss, fill_rgb, stroke_rgb)

        self.end_transform_to_tile()

    def draw_bridge_ramp(self, tile, rotation, payload):
        """
        Draw a bridge ramp for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the bridge ramp, in the range 0, 3.
        :type rotation: integer

        :param payload: The payload of the bridge. It should be one of 'rail', 'road'.
        :type payload: string.
        """

        bec = self.torb_edge_rgb
        bew = self.bridge_edge_width
        d = self.ss
        bd = 0.25 * d

        self.transform_to_tile(tile, rotation)

        self.draw_line(-0.25 * d, -bd, 0.5 * d, -bd, bec, bew)
        self.draw_line(-0.25 * d, bd, 0.5 * d, bd, bec, bew)

        if payload == "road":
            self.draw_road_line(-0.5 * d, 0, 0.5 * d, 0, line_mode="both", owner=tile.owner)
            if tile.occupant.tram_type == 1:
                self.draw_tram_line(-0.5 * d, 0, 0.5 * d, 0, owner=tile.owner_tram)
        else:
            track_type = tile.occupant.track_type
            self.draw_rail_line(
                -0.5 * d, 0, 0.5 * d, 0,
                track_type, line_mode="both", owner=tile.owner
            )

        self.end_transform_to_tile()

    def draw_bridge_over(self, tile, rotation, payload, track_type, has_tram, source_tile_owner):
        """
        Draw a bridge over a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the bridge, in the range 0, 1.
        :type rotation: integer

        :param payload: The payload of the bridge. It should be one of 'rail', 'road'.
        :type payload: string.

        :param has_tram: Whether the payload contains a tram.
        :type has_tram: Boolean
        """

        bec = self.torb_edge_rgb
        bew = self.bridge_edge_width
        d = self.ss
        bd = 0.25 * d

        self.transform_to_tile(tile, rotation)

        self.draw_line(-0.5 * d, -bd, 0.5 * d, -bd, bec, bew)
        self.draw_line(-0.5 * d, bd, 0.5 * d, bd, bec, bew)

        if payload == "road":
            self.draw_road_line(
                -0.5 * d, 0, 0.5 * d, 0,
                line_mode="both", owner=source_tile_owner
            )
            if has_tram:
                self.draw_tram_line(-0.5 * d, 0, 0.5 * d, 0, owner=source_tile_owner)
        else:
            self.draw_rail_line(
                -0.5 * d, 0, 0.5 * d, 0, track_type,
                line_mode="both", owner=source_tile_owner
            )

        self.end_transform_to_tile()

    def draw_tunnel_mouth(self, tile, rotation, payload):
        """
        Draw a tunnel mouth for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the tunnel mouth, in the range 0, 3.
        :type rotation: integer

        :param payload: The payload of the tunnel. It should be one of 'rail', 'road'.
        :type payload: string.
        """

        bec = self.torb_edge_rgb
        bew = self.bridge_edge_width
        d = self.ss

        self.transform_to_tile(tile, rotation)

        if payload == "road":
            self.draw_road_line(-0.5 * d, 0, 0.25 * d, 0, line_mode="both")
        else:
            track_type = tile.occupant.track_type
            self.draw_rail_line(
                -0.5 * d, 0, 0.25 * d, 0, track_type,
                line_mode="both", owner=tile.owner
            )

        bd = 0.3 * d
        self.draw_line(0.25 * d, -bd, 0.25 * d, bd, bec, bew)
        self.draw_line(0.25 * d, -bd, 0, -bd, bec, bew)
        self.draw_line(0.25 * d, bd, 0, bd, bec, bew)

        self.end_transform_to_tile()

    def draw_rail_bridge_ramp(self, tile, rotation):
        """
        Draw a rail bridge ramp for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the rail bridge ramp, in the range 0, 3.
        :type rotation: integer
        """

        self.draw_bridge_ramp(tile, rotation, "rail")

    def draw_rail_bridge_over(self, tile, rotation, track_type, source_tile_owner):
        """
        Draw a rail bridge over a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the rail bridge, in the range 0, 1.
        :type rotation: integer
        """

        self.draw_bridge_over(tile, rotation, "rail", track_type, None, source_tile_owner)

    def draw_rail_tunnel_mouth(self, tile, rotation):
        """
        Draw a rail tunnel mouth for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the tunnel mouth, in the range 0, 3.
        :type rotation: integer
        """

        self.draw_tunnel_mouth(tile, rotation, "rail")

    def draw_road_line(self, x1, y1, x2, y2, line_mode="outer", round_cap=False, owner=None):
        """
        Draw a line for a road.

        :param x1: The x coordinate of the start of the line.
        :type x1: float

        :param y1: The y coordinate of the start of the line.
        :type y1: float

        :param x2: The x coordinate of the end of the line.
        :type x2: float

        :param y2: The y coordinate of the end of the line.
        :type y2: float

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".

        :param round_cap: If True, set the line cap to round. Defaults to False.
        :type round_cap: Boolean

        :param owner: Owner of the road. Defaults to None.
        :type owner: Boolean
        """

        rw1 = 1.75 * self.road_width
        rw2 = 1.25 * self.road_width

        do_draw_inner = line_mode in ["inner", "both"]
        do_draw_outer = line_mode in ["outer", "both"]

        rgb = self.road_tile_rgb
        if owner is not None:
            rgb = self.player_colors[owner]

        if do_draw_outer:
            self.draw_line(x1, y1, x2, y2, rgb, rw1, round_cap)

        if do_draw_inner:
            self.draw_line(x1, y1, x2, y2, self.road_rgb, rw2, round_cap)

    def draw_tram_line(self, x1, y1, x2, y2, line_mode="outer", round_cap=False, owner=None):
        """
        Draw a line for a road.

        :param x1: The x coordinate of the start of the line.
        :type x1: float

        :param y1: The y coordinate of the start of the line.
        :type y1: float

        :param x2: The x coordinate of the end of the line.
        :type x2: float

        :param y2: The y coordinate of the end of the line.
        :type y2: float

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".

        :param round_cap: If True, set the line cap to round. Defaults to False.
        :type round_cap: Boolean

        :param owner: Owner of the road. Defaults to None.
        :type owner: Boolean
        """

        tw = self.tram_width
        rgb = self.tram_rgb
        if owner is not None:
            rgb = self.player_colors[owner]
        self.draw_line(x1, y1, x2, y2, rgb, tw, round_cap)

    def draw_road_NSEW(self, tile, rotation, line_mode, round_cap):
        """
        Draw a road for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the road, in the range 0, 3.
        :type rotation: integer

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".

        :param round_cap: If True, set the line cap to round. Defaults to False.
        :type round_cap: Boolean
        """

        self.transform_to_tile(tile, rotation)

        self.draw_road_line(0, 0.5 * self.ss, 0, 0, line_mode=line_mode, round_cap=False, owner=tile.owner)

        self.end_transform_to_tile()

    def draw_road_NE(self, tile, line_mode):
        """
        Draw a road in the NE direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_road_NSEW(tile, 3, line_mode=line_mode, round_cap=False)

    def draw_road_NW(self, tile, line_mode):
        """
        Draw a road in the NW direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_road_NSEW(tile, 2, line_mode=line_mode, round_cap=False)

    def draw_road_SE(self, tile, line_mode):
        """
        Draw a road in the SE direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_road_NSEW(tile, 0, line_mode=line_mode, round_cap=False)

    def draw_road_SW(self, tile, line_mode):
        """
        Draw a road in the SW direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_road_NSEW(tile, 1, line_mode=line_mode, round_cap=False)

    def draw_road_through(self, tile, line_mode, rotation):
        """
        Draw a road that goes across a given tile in the NE-SW direction.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean

        :param rotation: The direction of the road. Should be in the range [0, 1].
        :type rotation: integer
        """

        d = 0.5 * self.ss
        self.transform_to_tile(tile, rotation)

        self.draw_road_line(0, -d, 0, d, line_mode=line_mode, round_cap=False, owner=tile.owner)

        self.end_transform_to_tile()

    def draw_road_NE_to_SW(self, tile, line_mode):
        """
        Draw a road that goes across a given tile in the NE-SW direction.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_road_through(tile, line_mode, 1)

    def draw_road_NW_to_SE(self, tile, line_mode):
        """
        Draw a road that goes across a given tile in the NE-SW direction.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_road_through(tile, line_mode, 0)

    def draw_tram_NSEW(self, tile, rotation, line_mode, round_cap):
        """
        Draw a tram for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the road, in the range 0, 3.
        :type rotation: integer

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".

        :param round_cap: If True, set the line cap to round. Defaults to False.
        :type round_cap: Boolean
        """

        self.transform_to_tile(tile, rotation)

        self.draw_tram_line(0, 0.5 * self.ss, 0, 0, line_mode=line_mode, round_cap=True, owner=tile.owner_tram)

        self.end_transform_to_tile()

    def draw_tram_NE(self, tile, line_mode):
        """
        Draw a road in the NE direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_tram_NSEW(tile, 3, line_mode=line_mode, round_cap=False)

    def draw_tram_NW(self, tile, line_mode):
        """
        Draw a road in the NW direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_tram_NSEW(tile, 2, line_mode=line_mode, round_cap=False)

    def draw_tram_SE(self, tile, line_mode):
        """
        Draw a road in the SE direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_tram_NSEW(tile, 0, line_mode=line_mode, round_cap=False)

    def draw_tram_SW(self, tile, line_mode):
        """
        Draw a road in the SW direction for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is "outer".
        """

        self.draw_tram_NSEW(tile, 1, line_mode=line_mode, round_cap=False)

    def draw_road_depot(self, tile, rotation, line_mode):
        """
        Draw a road depot for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the depot, in the range 0, 3.
        :type rotation: integer
        """

        ss = self.ss

        if line_mode == "outer":
            self.draw_square(tile, self.road_depot_rgb, rgb_stroke=self.player_colors[tile.owner])

        self.transform_to_tile(tile, rotation)
        self.draw_road_line(0, 0, 0, 0, line_mode=line_mode, round_cap=True, owner=tile.owner)
        self.draw_road_line(0, 0, 0.5 * ss, 0, round_cap=False, line_mode=line_mode, owner=tile.owner)

        if tile.occupant.tram_type == 1:
            self.draw_tram_line(0, 0, 0.5 * ss, 0, round_cap=True, line_mode="outer", owner=tile.owner)

        self.end_transform_to_tile()

    def draw_road_bridge_ramp(self, tile, rotation):
        """
        Draw a road bridge ramp for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the triangle, in the range 0, 1.
        :type rotation: integer
        """

        self.draw_bridge_ramp(tile, rotation, "road")

    def draw_road_bridge_over(self, tile, rotation, has_tram, source_tile_owner):
        """
        Draw a road bridge over a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the bridge, in the range 0, 1.
        :type rotation: integer
        """

        self.draw_bridge_over(tile, rotation, "road", None, has_tram, source_tile_owner)

    def draw_road_tunnel_mouth(self, tile, rotation):
        """
        Draw a road tunnel mouth for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the tunnel mouth, in the range 0, 3.
        :type rotation: integer
        """

        self.draw_tunnel_mouth(tile, rotation, "road")

    def draw_level_crossing(self, tile, rotation):
        """
        Draw a level crossing for a given tile.

        :param tile: The tile to consider.
        :type tile: TileObject

        :param rotation: The direction of the level crossing, in the range 0, 1.
        :type rotation: integer
        """

        if rotation == 0:
            self.draw_road_NE_to_SW(tile, line_mode="both")

            if tile.owner_tram:
                self.draw_tram_NE(tile, line_mode="both")
                self.draw_tram_SW(tile, line_mode="both")

            self.draw_rail_Y(tile, line_mode="both")
        else:
            self.draw_road_NW_to_SE(tile, line_mode="both")

            if tile.owner_tram:
                self.draw_tram_NW(tile, line_mode="both")
                self.draw_tram_SE(tile, line_mode="both")

            self.draw_rail_X(tile, line_mode="both")

    def seek_bridge_ramp(self, tiles, row, col, rotation):
        """
        Recursively step through tiles to find a bridge ramp, and return the bridge ramp tile.

        :param tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.

        :param row: The row of the current tile.
        :type row: integer

        :param col: The col of the current tile.
        :type col: integer

        :param rotation: The direction of the bridge, in the range 0, 1.
        :type rotation: integer

        :return: The TileObject to the NE of the given tile.
        :rtype: TileObject
        """

        if rotation == 0:
            drow = 0
            dcol = 1
        else:
            drow = 1
            dcol = 0

        while True:
            index = self.parent.ncols * row + col

            try:
                tile = tiles[index]
            except IndexError:
                return None

            if tile.kind == 9:
                return tile

            row += drow
            col += dcol

    def draw_unknown_bridge_over(self, tiles, tile, rotation, line_mode="outer"):
        """
        Draw a bridge over a tile when we we don't know what the payload of the bridge is.

        :param tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.

        :param tile: The current tile.
        :type tile: integer

        :param rotation: The direction of the bridge, in the range 0, 1.
        :type rotation: integer

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean Default is False.
        """

        source_tile = self.seek_bridge_ramp(tiles, tile.row, tile.col, rotation)
        payload_kind = 0
        track_type = 0
        has_tram = False
        source_tile_owner = None

        if source_tile:
            payload_kind = source_tile.occupant.payload_kind
            source_tile_owner = source_tile.owner
            if payload_kind == 0:
                track_type = source_tile.occupant.track_type
            if source_tile.occupant.tram_type == 1:
                has_tram = True

        if payload_kind == 0:
            self.draw_rail_bridge_over(tile, rotation, track_type, source_tile_owner)
        elif payload_kind == 1:
            self.draw_road_bridge_over(tile, rotation, has_tram, source_tile_owner)

    def draw_tile_edge(self, tile, rotation, owner):
        """
        Draw the edge of a tile.

        :param tile: The current tile.
        :type tile: integer

        :param rotation: The direction of the edge, in the range [0, 7].
        :type rotation: integer

        :param owner: The owner index. Can be None.
        :type owner: integer
        """

        d = self.ds + 0.5
        ew = self.edge_width
        dew = (ew - 1) // 2
        rgb = self.industry_edge_rgb
        if owner is not None:
            rgb = self.player_colors[owner]

        self.transform_to_tile(tile, rotation)

        if rotation == 0:
            self.draw_rectangle(-d, -d - dew, self.ss, ew, rgb)
        elif rotation < 4:
            self.draw_rectangle(-d, -d, self.ss, ew, rgb)
        elif rotation == 4:
            self.draw_rectangle(-d, -d - dew, ew, ew, rgb)
        elif rotation == 5:
            self.draw_rectangle(-d - dew, -d, ew, ew, rgb)
        else:
            self.draw_rectangle(-d, -d, ew, ew, rgb)

        self.end_transform_to_tile()

    def draw_industry_edge(self, tile, rotation):
        """
        Draw the edge of an industry tile.

        :param tile: The current tile.
        :type tile: integer

        :param rotation: The direction of the edge, in the range [0, 7].
        :type rotation: integer
        """

        self.draw_tile_edge(tile, rotation, None)

    def draw_station_edge(self, tile, rotation):
        """
        Draw the edge of a station tile.

        :param tile: The current tile.
        :type tile: integer

        :param rotation: The direction of the edge, in the range [0, 7].
        :type rotation: integer
        """

        self.draw_tile_edge(tile, rotation, tile.owner)

    def draw_industry_edges(self, tile, tiles):
        """
        Draw all the edges of an industry tile.

        :param tile: The current tile.
        :type tile: integer

        :param tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.
        """

        industry_id = tile.occupant.industry_id
        for direction in range(8):
            other_tile = self.parent.tile_grid.get_tile_dir(tile, direction)
            if not other_tile:
                continue

            is_same_industry = other_tile.kind == 8 and other_tile.occupant.industry_id == industry_id
            if is_same_industry:
                continue
            self.draw_industry_edge(tile, direction)

    def draw_station_edges(self, tile, tiles):
        """
        Draw all the edges of a station tile.

        :param tile: The current tile.
        :type tile: integer

        :param tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.
        """

        station_id = tile.occupant.station_id
        for direction in range(8):
            other_tile = self.parent.tile_grid.get_tile_dir(tile, direction)
            if not other_tile:
                continue
            is_same_station = other_tile.kind == 5 and other_tile.occupant.station_id == station_id
            if is_same_station:
                continue
            self.draw_station_edge(tile, direction)

    def make_industry_shapes(self, industry_tiles):
        """
        Return a list of shapes for all the industries on the map, one shape per industry.

        :param industry_tiles: The list of all TileObjects in the map that contains an industry.
        :type industry_tiles: list of TileObject.

        :return: A list of list of TileObjects, one list per industry.
        :rtype: list of lists of TileObjects
        """

        industry_shapes_dict = {}
        for industry_tile in industry_tiles:
            industry_shapes_dict[industry_tile.occupant.industry_id] = []

        for industry_tile in industry_tiles:
            industry_shapes_dict[industry_tile.occupant.industry_id].append(industry_tile)

        industry_shapes_list = []
        for industry_id in industry_shapes_dict:
            industry_shapes_list.append(industry_shapes_dict[industry_id])

        return industry_shapes_list

    def make_station_shapes(self, station_tiles):
        """
        Return a list of shapes for all the stations on the map, one shape per station.

        :param station_tiles: The list of all TileObjects in the map that contains a station.
        :type station_tiles: list of TileObject.

        :return: A list of list of TileObjects, one list per station.
        :rtype: list of lists of TileObjects
        """

        station_shapes_dict = {}
        for station_tile in station_tiles:
            station_shapes_dict[station_tile.occupant.station_id] = []

        for station_tile in station_tiles:
            station_shapes_dict[station_tile.occupant.station_id].append(station_tile)

        station_shapes_list = []
        for station_id in station_shapes_dict:
            station_shapes_list.append(station_shapes_dict[station_id])

        return station_shapes_list

    def draw_tile_backgrounds(self, tiles):
        """
        Draw the background squares for all the tiles.

        :param tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            h = tile.height
            h_index = (h - self.parent.min_height) / (self.parent.max_height - self.parent.min_height)

            rgb_rand_1 = random.randint(0, self.ocean_noise)

            rgb_h = 255 - 55 * h_index
            if self.screen_mode == "dark":
                rgb_h = 55 * h_index
            height_rgb = (rgb_h, rgb_h, rgb_h)

            water_rgb = (rgb_rand_1, rgb_rand_1, 255)
            if self.screen_mode == "dark":
                water_rgb = (rgb_rand_1 // 2, rgb_rand_1 // 2, 150)

            fillColors = [
                height_rgb,              # Ground
                height_rgb,              # Rail
                self.road_tile_rgb,      # Road
                height_rgb,              # Town building
                height_rgb,              # Trees
                self.station_rgb,        # Stations
                water_rgb,               # Water
                height_rgb,              # Void
                self.industry_rgb,       # Industries
                self.torb_rgb,           # Tunnel/bridge
                height_rgb,              # Objects
            ]
            fillColor = fillColors[tile.kind % len(fillColors)]
            if tile.kind == 1:
                rail = tile.occupant
                if rail.is_depot:
                    fillColor = self.rail_depot_rgb

            if tile.kind == 5:
                station = tile.occupant
                if station.station_type == 0:
                    fillColor = self.rail_station_rgb
                if station.station_type == 1:
                    fillColor = self.airport_rgb
                if station.station_type == 2:
                    fillColor = self.bus_station_rgb
                if station.station_type == 3:
                    fillColor = self.truck_station_rgb
                if station.station_type == 4:
                    fillColor = self.heliport_rgb
                if station.station_type == 5:
                    fillColor = self.seaport_rgb

            self.draw_square(tile, fillColor)
            if tile.kind == 1:
                rail = tile.occupant
                if not rail.is_depot:
                    self.draw_rail_background(tile)

    def draw_rail_tile_lines(self, tiles, line_mode):
        """
        Draw the rail lines.

        :param tiles: The list of rail TileObjects in the map.
        :type tiles: list of TileObject.

        :param line_mode: Whether to draw the outer or inner line for the rail.
        :type line_mode: Boolean
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            rail = tile.occupant

            if rail.is_depot:
                self.draw_rail_depot(tile, rail.depot_direction)
            else:
                if rail.track_X:
                    self.draw_rail_X(tile, line_mode=line_mode)
                if rail.track_Y:
                    self.draw_rail_Y(tile, line_mode=line_mode)
                if rail.track_N:
                    self.draw_rail_N(tile, line_mode=line_mode)
                if rail.track_S:
                    self.draw_rail_S(tile, line_mode=line_mode)
                if rail.track_W:
                    self.draw_rail_W(tile, line_mode=line_mode)
                if rail.track_E:
                    self.draw_rail_E(tile, line_mode=line_mode)

    def draw_rail_signals(self, tiles):
        """
        Draw the rail lines.

        :param tiles: The list of rail TileObjects in the map.
        :type tiles: list of TileObject.
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            self.draw_rail_signals_tile(tile, rotation=0)

    def draw_road_tile_lines(self, tiles, line_mode):
        """
        Draw the road lines.

        :param tiles: The list of road TileObjects in the map.
        :type tiles: list of TileObject.
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            road = tile.occupant

            if road.is_depot:
                self.draw_road_depot(tile, road.depot_direction, line_mode=line_mode)

            elif road.is_level_crossing:
                self.draw_level_crossing(tile, road.level_crossing_direction)

            else:
                has_stub = False

                if road.road_NW and not road.road_SE:
                    has_stub = True
                if road.road_SW and not road.road_NE:
                    has_stub = True
                if road.road_SE and not road.road_NW:
                    has_stub = True
                if road.road_NE and not road.road_SW:
                    has_stub = True

                if has_stub:
                    self.transform_to_tile(tile, 0)
                    self.draw_road_line(0, 0, 0, 0, line_mode=line_mode, round_cap=True, owner=tile.owner)
                    self.end_transform_to_tile()

                if road.road_NW and not road.road_SE:
                    self.draw_road_NW(tile, line_mode)
                if road.road_SW and not road.road_NE:
                    self.draw_road_SW(tile, line_mode)
                if road.road_SE and not road.road_NW:
                    self.draw_road_SE(tile, line_mode)
                if road.road_NE and not road.road_SW:
                    self.draw_road_NE(tile, line_mode)

                if road.road_NW and road.road_SE:
                    self.draw_road_NW_to_SE(tile, line_mode)
                if road.road_SW and road.road_NE:
                    self.draw_road_NE_to_SW(tile, line_mode)

    def draw_tram_tile_lines(self, tiles, line_mode):
        """
        Draw the tram lines.

        :param tiles: The list of road TileObjects in the map.
        :type tiles: list of TileObject.
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            road = tile.occupant

            if road.is_depot:
                continue

            elif road.is_level_crossing:
                continue

            else:
                if road.tram_NW:
                    self.draw_tram_NW(tile, line_mode)
                if road.tram_SW:
                    self.draw_tram_SW(tile, line_mode)
                if road.tram_SE:
                    self.draw_tram_SE(tile, line_mode)
                if road.tram_NE:
                    self.draw_tram_NE(tile, line_mode)

    def draw_stations_with_lines(self, tiles, all_tiles, line_mode="both"):
        """
        Draw the stations with lines.

        :param tiles: The list of stations TileObjects in the map.
        :type tiles: list of TileObject.

        :param all_tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.

        :param line_mode: Whether to draw the outer or inner line for the payload.
        :type line_mode: Boolean
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            station = tile.occupant
            self.draw_station_edges(tile, all_tiles)

            if station.station_type == 0:
                if station.track_direction == 0:
                    self.draw_rail_X(tile, line_mode="both")
                else:
                    self.draw_rail_Y(tile, line_mode="both")

            elif station.station_type in [2, 3]:
                has_stub = False

                if station.road_NW and not station.road_SE:
                    has_stub = True
                if station.road_SW and not station.road_NE:
                    has_stub = True
                if station.road_SE and not station.road_NW:
                    has_stub = True
                if station.road_NE and not station.road_SW:
                    has_stub = True

                if has_stub:
                    self.transform_to_tile(tile, 0)
                    self.draw_road_line(0, 0, 0, 0, line_mode=line_mode, round_cap=True, owner=tile.owner)
                    self.end_transform_to_tile()

                if station.road_NW and not station.road_SE:
                    self.draw_road_NW(tile, line_mode="both")

                if station.road_SW and not station.road_NE:
                    self.draw_road_SW(tile, line_mode="both")

                if station.road_SE and not station.road_NW:
                    self.draw_road_SE(tile, line_mode="both")

                if station.road_NE and not station.road_SW:
                    self.draw_road_NE(tile, line_mode="both")

                if station.road_NW and station.road_SE:
                    self.draw_road_NW_to_SE(tile, line_mode="both")

                if station.road_SW and station.road_NE:
                    self.draw_road_NE_to_SW(tile, line_mode="both")

            if station.station_type == 7:
                if station.track_direction == 0:
                    self.draw_rail_X(tile, line_mode="inner")
                else:
                    self.draw_rail_Y(tile, line_mode="inner")

        # Draw tram lines last, to make sure they fit over the roads.
        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            station = tile.occupant

            if station.station_type in [2, 3]:
                if tile.occupant.tram_type == 1:
                    if station.road_NW:
                        self.draw_tram_NW(tile, line_mode="both")

                    if station.road_SW:
                        self.draw_tram_SW(tile, line_mode="both")

                    if station.road_SE:
                        self.draw_tram_SE(tile, line_mode="both")

                    if station.road_NE:
                        self.draw_tram_NE(tile, line_mode="both")

    def draw_tunnel_mouths_and_bridge_ramps(self, tiles):
        """
        Draw the tunnel mouths and bridge ramps.

        :param tiles: The list of tunnel or bridge TileObjects in the map.
        :type tiles: list of TileObject.
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            torb = tile.occupant

            if torb.is_tunnel:
                if torb.payload_kind == 0:
                    self.draw_rail_tunnel_mouth(tile, torb.entrance_direction)
                elif torb.payload_kind == 1:
                    self.draw_road_tunnel_mouth(tile, torb.entrance_direction)
            else:
                if torb.payload_kind == 0:
                    self.draw_rail_bridge_ramp(tile, torb.entrance_direction)
                elif torb.payload_kind == 1:
                    self.draw_road_bridge_ramp(tile, torb.entrance_direction)

    def draw_bridges_over(self, tiles):
        """
        Draw the bridges over tiles, where they exist.

        :param tiles: The list of all TileObjects in the map.
        :type tiles: list of TileObject.
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            if tile.bridge:
                self.draw_unknown_bridge_over(tiles, tile, tile.bridge - 1)

    def draw_industry_tiles(self, tiles, all_tiles):
        """
        Draw the industry tiles.

        :param tiles: The list of industry TileObjects in the map.
        :type tiles: list of TileObject.

        :param all_tiles: The list of all TileObjects in the map.
        :type all_tiles: list of TileObject.
        """

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            self.draw_industry_edges(tile, all_tiles)

    def draw_building_tiles(self, tiles):
        """
        Draw the industry tiles.

        :param tiles: The list of building TileObjects in the map.
        :type tiles: list of TileObject.
        """

        d = 0.3 * self.ss

        abar = self.get_progress_bar(tiles)

        for tile in tiles:
            abar()

            self.transform_to_tile(tile, 0)

            self.draw_rectangle(-d, -d, 2 * d, 2 * d, self.town_building_rgb)

            self.end_transform_to_tile()

    def draw_label(self, text, font_size, cx, cy):
        """
        Draw a label.

        :param text: The text of the label.
        :type text: string.

        :param font_size: The font size of the label.
        :type font_size: float.

        :param cx: The centre x value of the label.
        :type cx: float.

        :param cy: The centre y value of the label.
        :type cy: float.
        """

        context = self.context
        context.select_font_face(
            "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
        )
        context.set_font_size(font_size)
        (tx, ty, tw, th, tdx, tdy) = context.text_extents(text)

        padding = 0.1 * self.ss
        x = cx - tw / 2 - padding
        y = cy - th / 2 - padding

        self.draw_rectangle_rgba(x, y, tw + 2 * padding, th + 2 * padding, (255, 255, 255, 0.5))

        context.set_source_rgb(0, 0, 0)
        context.move_to(cx - tw / 2, cy + 0.25 * font_size)
        context.show_text(text)

    def draw_industry_labels(self):
        """Draw the industry labels."""

        for shape in self.industry_shapes:
            ave_row = sum([t.row for t in shape]) / len(shape)
            ave_col = sum([t.col for t in shape]) / len(shape)
            cx, cy = self.cxy_from_rc(ave_row, ave_col)
            font_size = 0.5 * self.ss

            context = self.context
            context.save()

            label = shape[0].occupant.industry_type
            label = label.replace("_", " ")
            label = label.lower().capitalize()

            self.draw_label(label, font_size, cx, cy)

            context.restore()

    def draw_station_labels(self):
        """Draw the station labels."""

        for shape in self.station_shapes:
            ave_row = sum([t.row for t in shape]) / len(shape)
            ave_col = sum([t.col for t in shape]) / len(shape)
            cx, cy = self.cxy_from_rc(ave_row, ave_col)
            font_size = 0.5 * self.ss

            context = self.context
            context.save()

            label = "Station"
            label = label.replace("_", " ")
            label = label.lower().capitalize()

            self.draw_label(label, font_size, cx, cy)

            context.restore()

    def save_image(self, image_file_path, filetype="PNG"):
        """
        Save the image to file.

        :param image_file_path: The path to the file, excluding the extension.
        :type image_file_path: string.

        :param filetype: The filetype to the image. Defaults to 'PNG'.
        :type filetype: string.

        :return: A list of list of TileObjects, one list per industry.
        :rtype: list of lists of TileObjects
        """

        iw = self.ss * (self.parent.ncols - 1)
        ih = self.ss * (self.parent.nrows - 1)

        logline = f"Dimensions of tile size, image before resizing: {self.ss}, {iw} x {ih}"
        self.log_message(logline)

        max_dimension = max(iw, ih)
        if max_dimension > 32767:
            rho = 32767 / max_dimension
            self.ss = int(rho * self.ss)
            self.ds = int(rho * self.ds)
            iw = self.ss * (self.parent.ncols - 1)
            ih = self.ss * (self.parent.nrows - 1)

        logline = f"Dimensions of tile size, image after resizing : {self.ss}, {iw} x {ih}"
        self.log_message(logline)

        if filetype == "PNG":
            self.image = cairo.ImageSurface(cairo.FORMAT_ARGB32, iw, ih)
        elif filetype == "SVG":
            self.image = cairo.SVGSurface(f"{image_file_path}", iw, ih)

        self.context = cairo.Context(self.image)

        all_tiles = self.parent.tiles
        rail_tiles = [t for t in all_tiles if t.kind == 1]
        road_tiles = [t for t in all_tiles if t.kind == 2]
        building_tiles = [t for t in all_tiles if t.kind == 3]
        stations_tiles = [t for t in all_tiles if t.kind == 5]
        industry_tiles = [t for t in all_tiles if t.kind == 8]
        torb_tiles = [t for t in all_tiles if t.kind == 9]

        self.industry_shapes = self.make_industry_shapes(industry_tiles)
        self.station_shapes = self.make_station_shapes(stations_tiles)

        self.log_message("Drawing tile backgrounds.")
        self.draw_tile_backgrounds(all_tiles)

        self.log_message("Drawing road tiles.")
        self.draw_road_tile_lines(road_tiles, line_mode="outer")

        self.log_message("Drawing rail tiles.")
        self.draw_rail_tile_lines(rail_tiles, line_mode="outer")

        self.log_message("Drawing station tiles.")
        self.draw_stations_with_lines(stations_tiles, all_tiles)

        self.log_message("Drawing tunnel mouth and bridge ramp tiles.")
        self.draw_tunnel_mouths_and_bridge_ramps(torb_tiles)

        self.log_message("Drawing building tiles.")
        self.draw_building_tiles(building_tiles)

        self.log_message("Drawing industry tiles.")
        self.draw_industry_tiles(industry_tiles, all_tiles)

        self.log_message("Drawing road tiles.")
        self.draw_road_tile_lines(road_tiles, line_mode="inner")

        self.log_message("Drawing tram tiles.")
        self.draw_tram_tile_lines(road_tiles, line_mode="inner")

        self.log_message("Drawing rail tiles.")
        self.draw_rail_tile_lines(rail_tiles, line_mode="inner")

        self.log_message("Drawing rail signals.")
        self.draw_rail_signals(rail_tiles)

        self.log_message("Drawing bridges over tiles.")
        self.draw_bridges_over(all_tiles)

        self.log_message("Drawing industry labels.")
        self.draw_industry_labels()

        # Station names don't work yet. I hope to add them in the future.
        # self.log_message("Drawing station labels.")
        # self.draw_station_labels()

        if filetype == "PNG":
            self.log_message("Writing PNG file to disk.")
            image_file_path = image_file_path.replace(".sav", ".png")
            self.image.write_to_png(image_file_path)
            self.log_message("All done!")
