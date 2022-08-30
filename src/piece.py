from enum import Enum, auto
from src.game import Game

from src.style import Style


class PType(Enum):
    I = auto()
    J = auto()
    L = auto()
    O = auto()
    S = auto()
    T = auto()
    Z = auto()


class Piece:
    def __init__(self, game: Game):
        self.type = type
        self.rotation = 0
        self.grid = generatePiece(type, self.rotation)
        self.x = 0
        self.y = 0
        self.blocks = game.style.drawPiece(self)

    def getCoords(self):
        coords = []
        for i in range(4):
            coords.append((self.grid[0][i], self.grid[1][i]))
        return coords


def generatePiece(p: PType, rot: int = 0):
    match p:
        case PType.I:
            if rot % 2 == 0:
                return (0, 1, 2, 3), (0, 0, 0, 0)
            else:
                return (0, 0, 0, 0), (0, 1, 2, 3)
        case PType.J:
            if rot == 0:
                return (0, 1, 2, 2), (0, 0, 0, 1)
            elif rot == 1:
                return (0, 1, 2, 0), (0, 0, 0, 0)
            elif rot == 2:
                return (0, 0, 1, 2), (0, 1, 1, 1)
            else:
                return (0, 1, 2, 2), (1, 1, 1, 0)
        case PType.L:
            if rot == 0:
                return (0, 1, 2, 0), (0, 0, 0, 1)
            elif rot == 1:
                return (0, 1, 2, 2), (0, 0, 0, 1)
            elif rot == 2:
                return (0, 1, 2, 2), (1, 1, 1, 0)
            else:
                return (0, 1, 2, 0), (1, 1, 1, 0)
        case PType.O:
            return (0, 1, 0, 1), (0, 0, 1, 1)
        case PType.S:
            if rot % 2 == 0:
                return (0, 1, 1, 2), (0, 0, 1, 1)
            else:
                return (0, 0, 1, 1), (0, 1, 1, 2)
        case PType.T:
            if rot == 0:
                return (0, 1, 2, 1), (0, 0, 0, 1)
            elif rot == 1:
                return (0, 1, 2, 1), (1, 1, 1, 0)
            elif rot == 2:
                return (0, 1, 2, 1), (1, 1, 1, 0)
            else:
                return (0, 1, 2, 1), (0, 0, 0, 1)
        case PType.Z:
            if rot % 2 == 0:
                return (0, 1, 1, 2), (1, 1, 0, 0)
            else:
                return (0, 0, 1, 1), (0, 1, 1, 2)
