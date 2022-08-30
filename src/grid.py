from piece import Piece, generateCoords


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[False for x in range(height)] for y in range(width)]
        self.pieces = [[None for x in range(height)] for y in range(width)]

    def getGrid(self):
        return self.grid

    def isBlock(self, x: int, y: int):
        return self.grid[x][y]

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
            self.grid[piece.x + x][piece.y + y] = True
            self.pieces[piece.x + x][piece.y + y] = piece
            clear = True
            for x2 in range(self.width):
                if not self.grid[x2][y]:
                    clear = False
                    break
            if not clear:
              continue
            for x2 in range(self.width):
                self.grid[x2][y] = False
                remove: Piece = self.pieces[x2][y]
                if not remove:
                  continue
                
                    

    def clear(self):
        self.grid = [[False for x in range(self.height)] for y in range(self.width)]
