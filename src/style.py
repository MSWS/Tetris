from abc import ABC, abstractmethod
from tkinter import Canvas
from grid import Grid
from piece import PType, Piece


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
    def coordToPixel(self, x, y):
        pass

    @abstractmethod
    def pixelToCoord(self, x, y):
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
        print(
            "Width: {}, Height: {}, PixelSize: {}, GridStart: {}, GridStop: {}".format(
                self.width, self.height, self.pixelSize, self.gridStart, self.gridStop
            )
        )

    def drawPiece(self, piece: Piece):
        pieces = piece.blocks or []
        if not len(piece.blocks):
            for x, y in piece.getCoords():
                x, y = self.coordToPixel(x + piece.x, y + piece.y)
                pieces.append(
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + self.pixelSize,
                        y + self.pixelSize,
                        fill=self.getColor(piece.type),
                    )
                )
                piece.blocks = pieces

        index = 0
        for x, y in piece.getCoords():
            x, y = self.coordToPixel(x + piece.x, y + piece.y)
            self.canvas.coords(
                piece.blocks[index], x, y, x + self.pixelSize, y + self.pixelSize
            )
            index += 1
        return pieces

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

    def clearBoard(self):
        self.canvas.delete("all")