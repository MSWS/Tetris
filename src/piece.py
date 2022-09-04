from enum import Enum, auto


class PType(Enum):
    """Represents the possible types of pieces"""
    I = auto()
    J = auto()
    L = auto()
    O = auto()
    S = auto()
    T = auto()
    Z = auto()


class Piece:
    """Represents a whole Piece that contains its type,
      (drawn) blocks, rotation, position, and coordinates
      """

    def __init__(self, x: int, style, ptype: PType) -> None:
        self.type = ptype
        self.rotation = 0
        self.grid = generate_piece(ptype, self.rotation)
        self.x = x
        self.y = 0
        self.blocks = []
        self.blocks = style.draw_piece(self)

    def get_coords(self) -> list[tuple[int, int]]:
        """Gets the coordinates that needed to draw at, see generateCoords"""
        coords = []
        for i in range(4):
            #pylint: disable=unsubscriptable-object
            coords.append((self.grid[0][i], self.grid[1][i]))
        return coords

    def get_block(self, x, y):
        """Get the (drawn) block at the specific GLOBAL coordinates
        throws an exception if no block belonging to the piece exists
        """
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
        raise Exception(f'Block not found at {x}, {y}')

    def rotate(self, counter=True) -> None:
        """Rotates the piece either clockwise or counter-clockwise
        and then updates the piece's grid
        """
        self.rotation += 1 if counter else -1
        if self.rotation < 0:
            self.rotation = 3
        self.rotation %= 4
        self.grid = generate_piece(self.type, self.rotation)

    def set_rotate(self, rotation: int) -> None:
        """Sets the rotation of the piece to the specified rotation, similar to rotate"""
        if self.rotation == rotation:
            return
        self.rotation = rotation
        self.grid = generate_piece(self.type, self.rotation)


class Block:
    """Data wrapper for a drawn block, holding the parent piece, x, y, and an arbitrary ID"""

    def __init__(self, piece: Piece, x: int, y: int, uid) -> None:
        self.piece = piece
        self.x = x
        self.y = y
        self.id = uid


def generate_coords(_p: PType, rot: int = 0) -> list[tuple[int, int]]:
    """Generates the (drawing) coordinates of a piece with the specified type and rotation"""
    grid = generate_piece(_p, rot)
    coords = []
    for i in range(4):
        #pylint: disable=unsubscriptable-object
        coords.append((grid[0][i], grid[1][i]))
    return coords


# pylint: disable=too-many-return-statements
def generate_piece(ptype: PType, rot: int = 0) -> tuple[tuple[int], tuple[int]]:
    """Generates the relative gamepay coordsintes of a piece with the specified type and rotation"""
    rot %= 4
    match ptype:
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
    raise Exception(
        f'Could not calculate piece of {ptype} with rotation {rot}')
