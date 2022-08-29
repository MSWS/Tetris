from piece import Piece, PType, generatePiece


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[]]
    
    def getGrid(self):
        return self.grid

    def isBlock(self, x: int, y: int):
        return self.grid[x][y]
    
    def tryFit(self, piece: Piece, rotate = False):
        for x, y in piece.getCoords():
            if self.isBlock(piece.x + x, piece.y + y):
                return False
        return True
