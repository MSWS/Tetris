from distutils.log import error
from enum import Enum, auto


class PType(Enum):
    I = auto()
    J = auto()
    L = auto()
    O = auto()
    S = auto()
    T = auto()
    Z = auto()


class Piece:
    def __init__(self, x: int, style, type: PType):
        self.type = type
        self.rotation = 0
        self.grid = generatePiece(type, self.rotation)
        self.x = x
        self.y = 0
        self.blocks = []
        self.blocks = style.drawPiece(self)

    def getCoords(self):
        coords = []
        for i in range(4):
            coords.append((self.grid[0][i], self.grid[1][i]))
        return coords

    def getBlock(self, x, y):
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
        raise Exception("Block not found at {}, {}".format(x, y))

    def rotate(self, counter=True):
        self.rotation += 1 if counter else -1
        if self.rotation < 0:
            self.rotation = 3
        self.rotation %= 4
        self.grid = generatePiece(self.type, self.rotation)

    def setRotate(self, rotation: int):
        self.rotation = rotation
        self.grid = generatePiece(self.type, self.rotation)

    def clearBlock(self, block):
        self.blocks.remove(block)


class Block:
    def __init__(self, piece: Piece, x: int, y: int, id):
        self.piece = piece
        self.x = x
        self.y = y
        self.id = id


def generateCoords(p: PType, rot: int = 0):
    grid = generatePiece(p, rot)
    coords = []
    for i in range(4):
        coords.append((grid[0][i], grid[1][i]))
    return coords


def generatePiece(p: PType, rot: int = 0):
    rot %= 4
    match p:
        case PType.I:
            if rot % 2 == 0:
                return (0, 1, 2, 3), (0, 0, 0, 0)
            else:
                return (1, 1, 1, 1), (0, 1, 2, 3)
        case PType.J:
            if rot == 0:
                return (0, 0, 1, 2), (1, 0, 0, 0)
            elif rot == 1:
                return (0, 1, 0, 0), (2, 2, 1, 0)
            elif rot == 2:
                return (0, 1, 2, 2), (1, 1, 1, 0)
            else:
                return (1, 1, 1, 0), (2, 1, 0, 0)
        case PType.L:
            if rot == 0:
                return (0, 1, 2, 2), (0, 0, 0, 1)
            elif rot == 1:
                return (0, 0, 0, 1), (2, 1, 0, 0)
            elif rot == 2:
                return (0, 0, 1, 2), (0, 1, 1, 1)
            else:
                return (0, 1, 1, 1), (2, 2, 1, 0)
        case PType.O:
            return (0, 1, 0, 1), (0, 0, 1, 1)
        case PType.S:
            if rot % 2 == 0:
                return (0, 1, 1, 2), (0, 0, 1, 1)
            else:
                return (0, 0, 1, 1), (2, 1, 1, 0)
        case PType.T:
            if rot == 0:
                return (0, 1, 1, 2), (0, 1, 0, 0)
            elif rot == 1:
                return (0, 0, 0, 1), (0, 1, 2, 1)
            elif rot == 2:
                return (0, 1, 2, 1), (1, 1, 1, 0)
            else:
                return (0, 1, 1, 1), (1, 2, 1, 0)
        case PType.Z:
            if rot % 2 == 0:
                return (0, 1, 1, 2), (1, 1, 0, 0)
            else:
                return (0, 0, 1, 1), (0, 1, 1, 2)
