import random
from grid import Grid
from piece import PType, Piece
from style import Style


class Game:
    def __init__(self, style: Style, grid: Grid) -> None:
        self.style = style
        self.grid = grid
        self.reset()
        self.pause = False
        self.bag = []

    def tick(self) -> None:
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

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                block = self.grid.blocks[y][x]
                if not block:
                    continue
                if block.x != x or block.y != y:
                    print(
                        "{} Block out of place internal: {}, grid: {}".format(
                            x, block.y, y
                        )
                    )

    def checkClear(self) -> None:
        self.grid.clearLines()
        self.style.clearLines()

    def reset(self) -> None:
        self.grid.clear()
        self.style.clearBoard()
        self.activePiece = None
        self.ticks = 0
        self.failTicks = 0
        self.score = 0
        self.alive = True
        self.style.drawBoundaries()

    def render(self) -> None:
        if self.activePiece:
            self.activePiece.blocks = self.style.drawPiece(self.activePiece, True)

    def generatePiece(self) -> Piece:
        type = self.getNextPiece()
        self.style.drawNext(self.bag)
        return Piece(self.grid.width // 2 - 1, self.style, type)

    def getNextPiece(self) -> PType:
        if len(self.bag) == 0:
            self.bag = list(PType)
            random.shuffle(self.bag)
        toMake = list(PType)
        for piece in self.bag:
            if piece in toMake:
                toMake.remove(piece)

        print(len(self.bag), self.bag)
        self.bag.insert(0, toMake[0] if len(toMake) > 0 else random.choice(list(PType)))
        return self.bag.pop()

    def onKey(self, event) -> None:
        if self.activePiece is None:
            return
        if event.keysym.lower() == "space":
            self.pause = not self.pause
            return
        if self.pause:
            return
        lastCoord = (self.activePiece.x, self.activePiece.y)
        lastRotate = self.activePiece.rotation
        targetRotation = lastRotate
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
                targetRotation = (self.activePiece.rotation + 3) % 4
            case "x":
                targetRotation = (self.activePiece.rotation + 1) % 4
            case _:
                print("Unknown key:", event.keysym.lower())
        if not self.grid.tryFit(self.activePiece, targetRotation):
            self.activePiece.x, self.activePiece.y = lastCoord
        else:
            self.activePiece.setRotate(targetRotation)
