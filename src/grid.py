from piece import PType, Piece, generate_coords


class Grid:
    """Internal boolean represntation of the game board where
      filled blocks are True and empty blocks are False
    """
    basicWallKick = [
        [(-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 0>>1
        [(1, 0), (1, -1), (0, 2), (1, 2)],  # 1>>0
        [(1, 0), (1, -1), (0, 2), (1, 2)],  # 1>>2
        [(-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 2>>1
        [(1, 0), (1, 1), (0, -2), (1, -2)],  # 2>>3
        [(-1, 0), (-1, -1), (0, 2), (-1, 2)],  # 3>>2
        [(-1, 0), (-1, -1), (0, 2), (-1, 2)],  # 3>>0
        [(1, 0), (1, 1), (0, -2), (1, -2)],  # 0>>3
    ]

    iWallKick = [
        [(-2, 0), (1, 0), (-2, -1), (1, 2)],  # 0>>1
        [(2, 0), (-1, 0), (2, 1), (-1, -2)],  # 1>>0
        [(-1, 0), (2, 0), (-1, 2), (2, -1)],  # 1>>2
        [(1, 0), (-2, 0), (1, -2), (-2, 1)],  # 2>>1
        [(2, 0), (-1, 0), (2, 1), (-1, -2)],  # 2>>3
        [(-2, 0), (1, 0), (-2, -1), (1, 2)],  # 3>>2
        [(1, 0), (-2, 0), (1, -2), (-2, 1)],  # 3>>0
        [(-1, 0), (2, 0), (-1, 2), (2, -1)],  # 0>>3
    ]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[False for y in range(width)] for x in range(height)]
        self.blocks = [[None for y in range(width)] for x in range(height)]
        self.to_delete = []

    def get_grid(self) -> list[list[bool]]:
        """Returns the grid"""
        return self.grid

    def is_block(self, x: int, y: int) -> bool:
        """Returns true if the given position has a block"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x]

    def try_fit(self, piece: Piece, rotation=None) -> bool:
        """Returns whether the piece can fit in the grid, if rotation is specified,
          it will use the hitbox from the given rotation, though will not rotate the piece itself
        """
        fits = True
        coords = generate_coords(
            piece.type, rotation if rotation is not None else piece.rotation
        )
        for x, y in coords:
            if piece.x + x < 0 or piece.x + x >= self.width:
                fits = False
                break
            if piece.y + y < 0 or piece.y + y >= self.height:
                fits = False
                break
            if self.is_block(piece.x + x, piece.y + y):
                fits = False
                break
        if fits:
            return True
        if rotation is None or rotation == piece.rotation:
            return False

        test_index = self.get_test_index(piece.rotation, rotation)
        #pylint: disable=invalid-sequence-index
        tests = (self.basicWallKick[test_index] if piece.type !=
                 PType.I else self.iWallKick[test_index])

        o_pos = (piece.x, piece.y)
        o_rot = piece.rotation
        for test_x, test_y in tests:
            piece.x += test_x
            piece.y -= test_y
            piece.set_rotate(rotation)
            if self.try_fit(piece, rotation):
                return True
            piece.x, piece.y = o_pos
            piece.set_rotate(o_rot)
        return False

    def get_test_index(self, old_rot: int, new_rot: int) -> int:
        """Returns the index of the wall kick tests to use"""
        match old_rot:
            case 0:
                return 0 if new_rot == 1 else 7
            case 1:
                return 1 if new_rot == 0 else 2
            case 2:
                return 3 if new_rot == 1 else 4
            case 3:
                return 5 if new_rot == 2 else 6

    def add_piece(self, piece: Piece) -> None:
        """Adds the piece to the grid"""
        for x, y in piece.get_coords():
            self.grid[piece.y + y][piece.x + x] = True
            self.blocks[piece.y + y][piece.x + x] = piece.get_block(
                piece.x + x, piece.y + y
            )

    def clear_lines(self) -> int:
        """Clears all lines that are full and returns the number of lines cleared"""
        cleared = 0
        for y in range(self.height):
            if not all(self.grid[y]):
                continue
            cleared += 1
            self.grid.pop(y)
            self.grid.insert(0, [False for x in range(self.width)])
            self.to_delete += self.blocks.pop(y)
            self.blocks.insert(0, [None for x in range(self.width)])

            for yy in range(y + 1):
                for block in self.blocks[yy]:
                    if block:
                        block.y += 1
            y -= 1
        return cleared

    def clear(self) -> None:
        """Clears the grid, meant for when the user tops out"""
        self.grid = [[False for y in range(self.width)]
                     for x in range(self.height)]
        self.blocks = [[None for y in range(self.width)]
                       for x in range(self.height)]
