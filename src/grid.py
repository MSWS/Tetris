from piece import Piece, generateCoords


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[False for x in range(width)] for y in range(height)]
        self.pieces = [[None for x in range(height)] for y in range(width)]

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
            self.pieces[piece.x + x][piece.y + y] = piece

    def clearLine(self, y: int):
        for x in range(self.width):
            self.grid[y][x] = False
            self.pieces[x][y] = None
        copy = self.grid
        for y in range(y):
            if y > 0:
                self.grid[y] = copy[y - 1]
            else:
                self.grid[y] = [False for x in range(self.width)]
        self.grid = copy

    def getClearLines(self, start=0):
        lines = {}
        for y in range(start, self.height):
            clear = True
            for x in range(self.width):
                if not self.grid[y][x]:
                    clear = False
                    break
            if clear:
                pieces = []
                for x in range(self.width):
                    pieces.append(self.pieces[x][y])
                lines[y] = pieces
        return lines

    def clear(self):
        self.grid = [[False for x in range(self.width)] for y in range(self.height)]
