from piece import Piece, generateCoords


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[False for y in range(width)] for x in range(height)]
        self.blocks = [[None for y in range(width)] for x in range(height)]

    def getGrid(self):
        return self.grid

    def isBlock(self, x: int, y: int):
        return self.grid[y][x]

    def tryFit(self, piece: Piece, rotate=-1):
        fits = True
        coords = (
            generateCoords(piece.type, piece.rotation + rotate)
            if rotate != -1
            else piece.getCoords()
        )
        for x, y in coords:
            if piece.x + x < 0 or piece.x + x >= self.width:
                fits = False
                break
            if piece.y + y < 0 or piece.y + y >= self.height:
                fits = False
                break
            if self.isBlock(piece.x + x, piece.y + y):
                fits = False
                break
        if not fits and rotate != -1:
            if rotate == 4:
                return False
            return self.tryFit(piece, rotate + 1)
        if fits and rotate != -1:
            piece.setRotate(piece.rotation + rotate)
        return fits

    def addPiece(self, piece: Piece):
        for x, y in piece.getCoords():
            self.grid[piece.y + y][piece.x + x] = True
            self.blocks[piece.y + y][piece.x + x] = piece.getBlock(
                piece.x + x, piece.y + y
            )

    def clearLine(self, y: int):
        self.grid[y] = [False for x in range(self.width)]
        gridCopy = self.grid.copy()
        blockCopy = self.blocks.copy()
        for by in range(1, y + 1):
            self.grid[by] = gridCopy[by - 1]
            self.blocks[by] = blockCopy[by - 1]
        self.grid[0] = [False for x in range(self.width)]

    def getClearLine(self, start=0):
        for y in range(start, self.height):
            if all(self.grid[y]):
                return y
        return -1

    def clear(self):
        self.grid = [[False for y in range(self.width)] for x in range(self.height)]
        self.blocks = [[None for y in range(self.width)] for x in range(self.height)]

    def toString(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += "X" if self.grid[y][x] else " "
            string += "\n"
        return string

    def blocksToString(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += "X" if self.grid[y][x] else " "
            string += "\n"
        return string
