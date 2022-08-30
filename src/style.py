from abc import ABC, abstractmethod
from tkinter import Canvas, Tk
from grid import Grid

from piece import Piece


class Style(ABC):
    name = "Undefined"

    def __init__(self, grid: Grid):
        self.grid = grid

    @abstractmethod
    def drawPiece(self, piece: Piece):
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


class RGBStyle(Style):
    name = "RGB"

    def __init__(self, grid: Grid, canvas: Canvas):
        super().__init__(grid)
        self.canvas = canvas
        self.gridStart = (0, 0)
        self.width, self.height = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()
        self.gridStop = (self.width / 4 * 3, self.height)
        self.pixelSize = min(self.gridStop[1] - self.gridStart[0],
                             (self.gridStop[0] - self.gridStart[0]) / self.grid.width)
        print("Width: {}, Height: {}, PixelSize: {}, GridStart: {}, GridStop: {}".format(
            self.width, self.height, self.pixelSize, self.gridStart, self.gridStop))

    def drawPiece(self, piece: Piece):
        color = "red"
        for x, y in piece.getCoords():
            x, y = self.coordToPixel(x + piece.x, y + piece.y)
            self.canvas.create_rectangle(
                x, y, x + self.pixelSize, y + self.pixelSize, fill=color)

    def drawBoundaries(self):
        self.canvas.create_rectangle(
            0, 0, self.width, self.height, fill="gray")

    def coordToPixel(self, x, y):
        return (x * self.pixelSize + self.gridStart[0], y * self.pixelSize + self.gridStart[1])

    def pixelToCoord(self, x, y):
        if x < self.gridStart[0] or x > self.gridStop[0] or y < self.gridStart[1] or y > self.gridStop[1]:
            return None
        return (int((x - self.gridStart[0]) / self.pixelSize), int((y - self.gridStart[1]) / self.pixelSize))
