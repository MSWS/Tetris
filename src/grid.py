from piece import Piece


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[False for x in range(height)] for y in range(width)]

    def getGrid(self):
        return self.grid

    def isBlock(self, x: int, y: int):
        return self.grid[x][y]

    def tryFit(self, piece: Piece, rotate=False):
        for x, y in piece.getCoords():
            if piece.x + x < 0 or piece.x + x >= self.width:
                return False
            if piece.y + y < 0 or piece.y + y >= self.height:
                return False
            if self.isBlock(piece.x + x, piece.y + y):
                return False
        return True
    
    def addPiece(self, piece: Piece):
      for x, y in piece.getCoords():
        self.grid[piece.x + x][piece.y + y] = True
