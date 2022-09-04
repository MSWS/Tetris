from enum import Enum

from grid import Grid
from piece import PType, Piece


class ScoreType(Enum):
    """Enum for the different types of scores."""
    SINGLE = 100
    DOUBLE = 300
    TRIPLE = 500
    TETRIS = 800
    TSPIN = 400
    TSPIN_MINI = 100
    BACK_TO_BACK = 0.5
    SOFT = 1
    HARD = 2
    PERFECT_CLEAR = 800


class ScoreSystem:
    """Scoring system helper"""

    def __init__(self) -> None:
        self.level = 0
        self.points = 0
        self.previous_moves = []

    def points_for(self, level: int) -> int:
        """Returns the points required to reach the given level"""
        return 400 * (level ** (5/2)) + (level**3)

    def add_score(self, grid: Grid, piece: Piece) -> int:
        if piece.type != PType.T:
            return 0
        return 1

    def get_move_types(self, grid: Grid, piece: Piece) -> list[ScoreType]:
        """Returns the type of move that was made"""
        clears = 0
        px, py = piece.x, piece.y
        perfect = True
        for y in range(grid.height):
            if perfect and not all(grid.grid[y]):
                perfect = False
            if all(grid.grid[y]):
                clears += 1
        if perfect:
            return [ScoreType.PERFECT_CLEAR]
        match clears:
            case 0:
                return [self.process_tmove(grid, piece)]
            case 1:
                return [ScoreType.SINGLE]
            case 2:
                return [ScoreType.DOUBLE]
            case 3:
                return [ScoreType.TRIPLE]
            case 4:
                return [ScoreType.TETRIS]

    def process_tmove(self, grid: Grid, piece: Piece) -> ScoreType:
        """Checks if a T-Move is a T-Spin"""
        if piece.type != PType.T:
            return None
        px, py = piece.x, piece.y

        point_a, point_b, point_c, point_d = None, None, None, None
        match piece.rotation:
            case 0:
                point_a = grid.is_block(px, py)
                point_b = grid.is_block(px + 2, py)
                point_c = grid.is_block(px, py + 2)
                point_d = grid.is_block(px + 2, py + 2)
            case 1:
                point_a = grid.is_block(px + 2, py)
                point_b = grid.is_block(px + 2, py + 2)
                point_c = grid.is_block(px, py)
                point_d = grid.is_block(px, py + 2)
            case 2:
                point_a = grid.is_block(px + 2, py + 2)
                point_b = grid.is_block(px, py + 2)
                point_c = grid.is_block(px + 2, py)
                point_d = grid.is_block(px, py)
            case _:
                point_a = grid.is_block(px, py + 2)
                point_b = grid.is_block(px, py)
                point_c = grid.is_block(px + 2, py + 2)
                point_d = grid.is_block(px + 2, py)
        if point_a and point_b and (point_c or point_d):
            return ScoreType.TSPIN
        if point_c and point_d and (point_a or point_b):
            return ScoreType.TSPIN_MINI
