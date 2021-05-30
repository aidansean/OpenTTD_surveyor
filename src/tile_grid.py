class TileGrid:
    def __init__(self, nrows, ncols, tiles):
        """
        Create a TileGrid.

        :param nrows: The number of rows in the map of tiles.
        :type nrows: integer.

        :param ncols: The number of columns in the map of tiles.
        :type ncols: integer.

        :param tiles: The array of map tiles.
        :type tiles: list of TileObject.
        """

        self.nrows = nrows
        self.ncols = ncols
        self.tiles = tiles
        self.grid = []

        row = []
        for i, tile in enumerate(tiles):
            row.append(tile)
            if len(row) == self.ncols:
                self.grid.append(row)
                row = []

    def get_tile_dcr(self, tile, drow, dcol):
        """
        Return the tile in the direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.

        :param drow: The change in the row coordinate.
        :type drow: integer.

        :param dcol: The change in the column coordinate.
        :type dcol: integer.
        """

        try:
            return self.grid[tile.row + drow][tile.col + dcol]
        except IndexError:
            return None

    def get_tile_NW(self, tile):
        """
        Return the tile in the NW direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, -1, 0)

    def get_tile_NE(self, tile):
        """
        Return the tile in the NE direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, 0, 1)

    def get_tile_SE(self, tile):
        """
        Return the tile in the SE direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, 1, 0)

    def get_tile_SW(self, tile):
        """
        Return the tile in the SW direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, 0, -1)

    def get_tile_N(self, tile):
        """
        Return the tile in the N direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, -1, -1)

    def get_tile_E(self, tile):
        """
        Return the tile in the E direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, -1, 1)

    def get_tile_S(self, tile):
        """
        Return the tile in the S direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, 1, 1)

    def get_tile_W(self, tile):
        """
        Return the tile in the W direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.
        """

        return self.get_tile_dcr(tile, 1, -1)

    def get_tile_dir(self, tile, direction):
        """
        Return the tile in an indexed direction from the given tile.

        :param tile: The tile to look from.
        :type tile: TileObject.

        :param direction: The indexed direction. Indices are: [NW, SW, SE, NE, E, N, W, S]
        :type direction: integer.
        """

        if direction == 0:
            return self.get_tile_NW(tile)
        if direction == 1:
            return self.get_tile_SW(tile)
        if direction == 2:
            return self.get_tile_SE(tile)
        if direction == 3:
            return self.get_tile_NE(tile)
        if direction == 4:
            return self.get_tile_E(tile)
        if direction == 5:
            return self.get_tile_N(tile)
        if direction == 6:
            return self.get_tile_W(tile)
        if direction == 7:
            return self.get_tile_S(tile)
        return None
