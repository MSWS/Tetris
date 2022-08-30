from cgitb import reset
from mimetypes import init
import random
from grid import Grid
from piece import PType, Piece
from style import Style


class Game:
    def __init__(self, style: Style, grid: Grid):
        self.style = style
        self.grid = grid
        self.reset()

    def tick(self):
        self.ticks += 1
        if self.ticks % 10 != 0:
            return
        if self.activePiece is None:
            self.activePiece = self.generatePiece()
            if not self.grid.tryFit(self.activePiece):
                self.reset()
            return
        self.activePiece.y += 1
        if not self.grid.tryFit(self.activePiece):
            self.activePiece.y -= 1
            self.failTicks += 1
            if self.failTicks > 3:
                self.grid.addPiece(self.activePiece)
                self.activePiece = None
                self.failTicks = 0
        else:
            self.failTicks = 0

    def reset(self):
        self.grid.clear()
        self.style.clearBoard()
        self.activePiece = None
        self.ticks = 0
        self.failTicks = 0
        self.score = 0
        self.alive = True
        self.style.drawBoundaries()

    def render(self):
        if self.activePiece:
            self.style.drawPiece(self.activePiece)

    def generatePiece(self):
        type = random.choice(
            [PType.I, PType.J, PType.L, PType.O, PType.S, PType.T, PType.Z]
        )
        return Piece(self, type)

    def onKey(self, event):
        if self.activePiece is None:
            return
        lastCoord = (self.activePiece.x, self.activePiece.y)
        lastRotate = self.activePiece.rotation
        match event.keysym:
            case "Left":
                self.activePiece.x -= 1
            case "Right":
                self.activePiece.x += 1
            case "Up":  # Hard drop
                while self.grid.tryFit(self.activePiece):
                    self.activePiece.y += 1
                self.activePiece.y -= 1
                self.style.drawPiece(self.activePiece)
                self.grid.addPiece(self.activePiece)
                self.activePiece = None
                return
            case "Down":  # Soft drop
                self.activePiece.y += 1
            case "z":
                self.activePiece.rotate(True)
            case "x":
                self.activePiece.rotate(False)
            case _:
                print("Unknown key: {}", event.keysym)
        if not self.grid.tryFit(
            self.activePiece, 0 if lastRotate != self.activePiece.rotation else -1
        ):
            self.activePiece.x, self.activePiece.y = lastCoord
            self.activePiece.setRotate(lastRotate)
