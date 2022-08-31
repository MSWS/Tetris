from abc import ABC, abstractmethod
from cmath import log
import enum
from tkinter import Canvas
from grid import Grid
from piece import Block, PType, Piece


class Style(ABC):
    name = "Undefined"

    def __init__(self, grid: Grid):
        self.grid = grid

    @abstractmethod
    def drawPiece(self, piece: Piece) -> list:
        pass

    @abstractmethod
    def drawBoundaries(self):
        pass

    @abstractmethod
    def drawBlock(self, x, y):
        pass

    @abstractmethod
    def coordToPixel(self, x, y):
        pass

    @abstractmethod
    def pixelToCoord(self, x, y):
        pass

    @abstractmethod
    def clearLine(self, y: int, pieces: list):
        pass

    @abstractmethod
    def clearBoard(self):
        pass


class RGBStyle(Style):
    name = "RGB"

    def __init__(self, grid: Grid, canvas: Canvas):
        super().__init__(grid)
        self.canvas = canvas
        self.gridStart = (0, 0)
        self.width, self.height = (
            self.canvas.winfo_reqwidth(),
            self.canvas.winfo_reqheight(),
        )
        self.gridStop = (self.width / 4 * 3, self.height)
        self.pixelSize = min(
            (self.gridStop[0] - self.gridStart[0]) / self.grid.width,
            (self.gridStop[1] - self.gridStart[1]) / self.grid.height,
        )
        self.gridStop = (
            self.pixelSize * self.grid.width,
            self.pixelSize * self.grid.height,
        )
        print(
            "Width: {}, Height: {}, PixelSize: {}, GridStart: {}, GridStop: {}".format(
                self.width, self.height, self.pixelSize, self.gridStart, self.gridStop
            )
        )

    def drawBlock(self, x: int, y: int, id, color):
        bx, by = self.coordToPixel(x, y)
        if not id:
            if y > 3:
                raise Exception(
                    "Block created lower than expected ({}, {})".format(x, y)
                )
            id = self.canvas.create_rectangle(
                bx, by, bx + self.pixelSize, by + self.pixelSize, fill=color
            )
            return id
        self.canvas.coords(id, bx, by, bx + self.pixelSize, by + self.pixelSize)
        return id

    def drawPiece(self, piece: Piece):
        index = 0
        blocks = []
        for x, y in piece.getCoords():
            b = Block(
                piece,
                piece.x + x,
                piece.y + y,
                self.drawBlock(
                    piece.x + x,
                    piece.y + y,
                    piece.blocks[index].id if index < len(piece.blocks) else None,
                    self.getColor(piece.type),
                ),
            )
            blocks.append(b)
            index += 1
        return blocks

    def drawBoundaries(self):
        self.canvas.create_rectangle(
            self.gridStart[0],
            self.gridStart[1],
            self.gridStop[0] - self.gridStart[0],
            self.gridStop[1] - self.gridStart[1],
            fill="gray",
        )

    def coordToPixel(self, x, y):
        return (
            x * self.pixelSize + self.gridStart[0],
            y * self.pixelSize + self.gridStart[1],
        )

    def pixelToCoord(self, x, y):
        if (
            x < self.gridStart[0]
            or x > self.gridStop[0]
            or y < self.gridStart[1]
            or y > self.gridStop[1]
        ):
            return None
        return (
            int((x - self.gridStart[0]) / self.pixelSize),
            int((y - self.gridStart[1]) / self.pixelSize),
        )

    def getColor(self, type: PType):
        match type:
            case PType.I:
                return "cyan"
            case PType.J:
                return "blue"
            case PType.L:
                return "orange"
            case PType.O:
                return "yellow"
            case PType.S:
                return "green"
            case PType.T:
                return "purple"
            case PType.Z:
                return "red"

    def clearLine(self, y: int, blocks: set[Block]):
        for by in range(len(blocks)):
            if by < y:
                print("{}: {}".format(by, blocks[by]))
                for block in blocks[by]:
                    if not block:
                        continue
                    block.y += 1
                    self.drawBlock(
                        block.x, block.y, block.id, self.getColor(block.piece.type)
                    )
        for bx in range(len(blocks[y])):
            if blocks[y][bx] is None:
                continue
            self.canvas.delete(blocks[y][bx].id)
            blocks[y][bx] = None

    def clearBoard(self):
        self.canvas.delete("all")
