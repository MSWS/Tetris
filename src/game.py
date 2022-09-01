import random
from grid import Grid
from piece import PType, Piece
from style import Style


class Game:
    def __init__(self, style: Style, grid: Grid):
        self.style = style
        self.grid = grid
        self.reset()
        self.lastGrid = ""
        self.pause = False

    def tick(self):
        self.ticks += 1
        if self.ticks % 10 != 0 or self.pause:
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
                self.checkClear()
                self.activePiece = None
                self.failTicks = 0
        else:
            self.failTicks = 0
        gs = self.grid.toString()
        bs = self.grid.blocksToString()
        if gs != bs:
            print("Grid and blocks don't match!")
            print("Grid:")
            print(gs)
            print("Blocks:")
            print(bs)
        elif gs != self.lastGrid:
            print(bs)
            self.lastGrid = gs

    def checkClear(self):
        line = self.grid.getClearLine()
        while line != -1:
            self.style.clearLine(line, self.grid.blocks)
            self.grid.clearLine(line)
            line = self.grid.getClearLine()

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
            self.activePiece.blocks = self.style.drawPiece(self.activePiece)

    def generatePiece(self):
        # type = random.choice(
        #     [PType.I, PType.J, PType.L, PType.O, PType.S, PType.T, PType.Z]
        # )
        type = PType.I
        return Piece(self, type)

    def onKey(self, event):
        if self.activePiece is None:
            return
        if event.keysym.lower() == "space":
            self.pause = not self.pause
            return
        if self.pause:
            return
        lastCoord = (self.activePiece.x, self.activePiece.y)
        lastRotate = self.activePiece.rotation
        match event.keysym.lower():
            case "left":
                self.activePiece.x -= 1
            case "right":
                self.activePiece.x += 1
            case "up":  # Hard drop
                while self.grid.tryFit(self.activePiece):
                    self.activePiece.y += 1
                self.activePiece.y -= 1
                self.activePiece.blocks = self.style.drawPiece(self.activePiece)
                self.grid.addPiece(self.activePiece)
                self.checkClear()
                self.activePiece = None
                return
            case "down":  # Soft drop
                self.activePiece.y += 1
            case "z":
                self.activePiece.rotate(False)
            case "x":
                self.activePiece.rotate(True)
            case _:
                print("Unknown key:", event.keysym.lower())
        if not self.grid.tryFit(
            self.activePiece, 0 if lastRotate != self.activePiece.rotation else -1
        ):
            self.activePiece.x, self.activePiece.y = lastCoord
            self.activePiece.setRotate(lastRotate)
