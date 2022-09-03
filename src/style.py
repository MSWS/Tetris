from abc import ABC, abstractmethod
from tkinter import Canvas
from grid import Grid
from piece import Block, PType, Piece, generatePiece


class Style(ABC):
    """An abstract class to allow for multiple styles of Tetris"""

    name = "Undefined"

    def __init__(self, grid: Grid):
        self.grid = grid

    @abstractmethod
    def drawPiece(self, piece: Piece, isActive=False) -> list[Block]:
        """Draws the specified piece on the canvas using its internal coordinates
        isActive is intended to allow for support for shadow/preview pieces
        """
        pass

    @abstractmethod
    def drawBoundaries(self) -> None:
        """Draws the boundaries of the grid, can also be used to stylize
        boundaries, grid, etc."""
        pass

    @abstractmethod
    def drawBlock(self, x, y) -> str:
        """Intended to draw a single block at a given coordinate, should be a generic method that
        returns a string ID that can be used to update the block later
        """
        pass

    @abstractmethod
    def coordToPixel(self, x, y) -> tuple[int, int]:
        """Converts a coordinate to a pixel"""
        pass

    @abstractmethod
    def pixelToCoord(self, x, y) -> tuple[int, int]:
        """Converts a pixel to a coordinate"""
        pass

    @abstractmethod
    def clearLines(self) -> None:
        """Clears the lines that have been filled, called AFTER grid clearLines is called"""
        pass

    @abstractmethod
    def clearBoard(self) -> None:
        """Clears the entire board, should reset the board to an empty grid"""
        pass

    @abstractmethod
    def drawNext(self, pieces: list[PType]) -> None:
        """Draws the next pieces in the queue"""
        pass


class RGBStyle(Style):
    name = "RGB"

    def __init__(self, grid: Grid, canvas: Canvas) -> None:
        super().__init__(grid)
        self.canvas = canvas
        self.gridStart = (0, 0)
        self.width, self.height = (
            self.canvas.winfo_reqwidth(),
            self.canvas.winfo_reqheight(),
        )
        self.gridStop = (int(self.width * 0.8), self.height)
        self.pixelSize = min(
            (self.gridStop[0] - self.gridStart[0]) / self.grid.width,
            (self.gridStop[1] - self.gridStart[1]) / self.grid.height,
        )
        self.gridStop = (
            self.pixelSize * self.grid.width,
            self.pixelSize * self.grid.height,
        )
        self.nextPieces = []
        self.previewPieces = []

    def drawBlock(self, x: int, y: int, id, color) -> str:
        bx, by = self.coordToPixel(x, y)
        if not id:
            id = self.canvas.create_rectangle(
                bx, by, bx + self.pixelSize, by + self.pixelSize, fill=color
            )
            return id
        if id not in self.canvas.find_all():
            raise Exception("Block ID not found ({})".format(id))
        if color:
            self.canvas.itemconfig(id, fill=color)
        self.canvas.coords(id, bx, by, bx + self.pixelSize, by + self.pixelSize)
        return id

    def drawPiece(self, piece: Piece, isActive=False) -> list[Block]:
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

        if not isActive:
            return blocks

        originalY = piece.y
        while self.grid.tryFit(piece):
            piece.y += 1
        piece.y -= 1

        index = 0
        for x, y in piece.getCoords():
            id = self.drawBlock(
                piece.x + x,
                piece.y + y,
                self.previewPieces[index] if index < len(self.previewPieces) else None,
                self.getColor(piece.type),
            )
            # Make preview piece transparent
            self.canvas.itemconfig(id, stipple="gray12")

            if id not in self.previewPieces:
                self.previewPieces.append(id)
            index += 1
        piece.y = originalY
        return blocks

    def drawBoundaries(self) -> None:
        self.canvas.create_rectangle(
            0, 0, self.width, self.height, fill="#333", outline="#ddd"
        )
        self.canvas.create_rectangle(
            self.gridStart[0],
            self.gridStart[1],
            self.gridStop[0] - self.gridStart[0],
            self.gridStop[1] - self.gridStart[1],
            fill="gray",
        )
        # Draw y coordinates
        for y in range(self.grid.height):
            self.canvas.create_text(
                self.gridStop[0] + 15,
                self.gridStart[1] + y * self.pixelSize,
                text=str(y),
                anchor="ne",
                fill="white",
            )

    def coordToPixel(self, x, y) -> tuple[int, int]:
        return (
            x * self.pixelSize + self.gridStart[0],
            y * self.pixelSize + self.gridStart[1],
        )

    def pixelToCoord(self, x, y) -> tuple[int, int]:
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

    def getColor(self, type: PType) -> str:
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

    def clearLines(self) -> None:
        for block in self.grid.toDelete:
            self.canvas.delete(block.id)
        self.grid.toDelete = []
        for by in range(self.grid.height):
            for block in self.grid.blocks[by]:
                if not block:
                    continue
                self.drawBlock(
                    block.x, block.y, block.id, self.getColor(block.piece.type)
                )

    def clearBoard(self) -> None:
        self.canvas.delete("all")
        self.nextPieces = []
        self.previewPieces = []

    def drawNext(self, pieces: list[PType]) -> None:
        for i in range(min(len(pieces), 4)):
            next = self.nextPieces[i] if i < len(self.nextPieces) else None
            type = pieces[len(pieces) - 1 - i]
            if not next:
                next = Piece(self.grid.width, self, type)
                self.nextPieces.append(next)
            next.x = self.grid.width + 1
            next.y = i * 4 + 1
            next.type = type
            next.grid = generatePiece(next.type)
            self.drawPiece(next)
