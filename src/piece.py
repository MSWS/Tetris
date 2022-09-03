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
    def __init__(self, x: int, style, type: PType) -> None:
        self.type = type
        self.rotation = 0
        self.grid = generatePiece(type, self.rotation)
        self.x = x
        self.y = 0
        self.blocks = []
        self.blocks = style.drawPiece(self)

    def getCoords(self) -> list[tuple[int, int]]:
        coords = []
        for i in range(4):
            coords.append((self.grid[0][i], self.grid[1][i]))
        return coords

    def getBlock(self, x, y) -> Block:
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
        raise Exception("Block not found at {}, {}".format(x, y))

    def rotate(self, counter=True) -> None:
        self.rotation += 1 if counter else -1
        if self.rotation < 0:
            self.rotation = 3
        self.rotation %= 4
        self.grid = generatePiece(self.type, self.rotation)

    def setRotate(self, rotation: int) -> None:
        self.rotation = rotation
        self.grid = generatePiece(self.type, self.rotation)

    def clearBlock(self, block) -> None:
        self.blocks.remove(block)


class Block:
    def __init__(self, piece: Piece, x: int, y: int, id) -> None:
        self.piece = piece
        self.x = x
        self.y = y
        self.id = id


def generateCoords(p: PType, rot: int = 0) -> list[tuple[int, int]]:
    grid = generatePiece(p, rot)
    coords = []
    for i in range(4):
        coords.append((grid[0][i], grid[1][i]))
    return coords


def generatePiece(p: PType, rot: int = 0) -> tuple[tuple[int], tuple[int]]:
    rot %= 4
    match p:
        case PType.I:
            match rot:
                case 0:
                    return (0, 1, 2, 3), (1, 1, 1, 1)
                case 1:
                    return (2, 2, 2, 2), (0, 1, 2, 3)
                case 2:
                    return (0, 1, 2, 3), (2, 2, 2, 2)
                case 3:
                    return (1, 1, 1, 1), (0, 1, 2, 3)
        case PType.J:
            match rot:
                case 0:
                    return (0, 0, 1, 2), (0, 1, 1, 1)
                case 1:
                    return (1, 2, 1, 1), (0, 0, 1, 2)
                case 2:
                    return (0, 1, 2, 2), (1, 1, 1, 2)
                case 3:
                    return (0, 1, 1, 1), (2, 2, 1, 0)
        case PType.L:
            match rot:
                case 0:
                    return (0, 1, 2, 2), (1, 1, 1, 0)
                case 1:
                    return (1, 1, 1, 2), (0, 1, 2, 2)
                case 2:
                    return (0, 0, 1, 2), (2, 1, 1, 1)
                case 3:
                    return (0, 1, 1, 1), (0, 0, 1, 2)
        case PType.O:
            return (1, 2, 1, 2), (0, 0, 1, 1)
        case PType.S:
            match rot:
                case 0:
                    return (0, 1, 1, 2), (1, 1, 0, 0)
                case 1:
                    return (1, 1, 2, 2), (0, 1, 1, 2)
                case 2:
                    return (0, 1, 1, 2), (2, 2, 1, 1)
                case 3:
                    return (0, 0, 1, 1), (0, 1, 1, 2)
        case PType.T:
            match rot:
                case 0:
                    return (0, 1, 1, 2), (1, 1, 0, 1)
                case 1:
                    return (1, 1, 1, 2), (0, 1, 2, 1)
                case 2:
                    return (0, 1, 1, 2), (1, 1, 2, 1)
                case 3:
                    return (0, 1, 1, 1), (1, 0, 1, 2)
        case PType.Z:
            match rot:
                case 0:
                    return (0, 1, 1, 2), (0, 0, 1, 1)
                case 1:
                    return (1, 1, 2, 2), (1, 2, 0, 1)
                case 2:
                    return (0, 1, 1, 2), (1, 1, 2, 2)
                case 3:
                    return (0, 0, 1, 1), (1, 2, 0, 1)
    raise Exception("Could not calculate piece of {} with rotation {}".format(p, rot))
