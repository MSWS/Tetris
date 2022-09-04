from abc import ABC, abstractmethod
from tkinter import Canvas
from grid import Grid
from piece import Block, Piece, PType, generate_piece


class Style(ABC):
    """An abstract class to allow for multiple styles of Tetris"""

    name = "Undefined"

    def __init__(self, grid: Grid):
        self.grid = grid

    @abstractmethod
    def draw_piece(self, piece: Piece, active=False) -> list[Block]:
        """Draws the specified piece on the canvas using its internal coordinates
        isActive is intended to allow for support for shadow/preview pieces
        """

    @abstractmethod
    def draw_boundaries(self) -> None:
        """Draws the boundaries of the grid, can also be used to stylize
        boundaries, grid, etc."""

    @abstractmethod
    def draw_block(self, x, y) -> str:
        """Intended to draw a single block at a given coordinate, should be a generic method that
        returns a string ID that can be used to update the block later
        """

    @abstractmethod
    def coord_pixel(self, x, y) -> tuple[int, int]:
        """Converts a coordinate to a pixel"""

    @abstractmethod
    def pixel_coord(self, x, y) -> tuple[int, int]:
        """Converts a pixel to a coordinate"""

    @abstractmethod
    def clear_lines(self) -> None:
        """Clears the lines that have been filled, called AFTER grid clearLines is called"""

    @abstractmethod
    def clear_board(self) -> None:
        """Clears the entire board, should reset the board to an empty grid"""

    @abstractmethod
    def draw_next(self, pieces: list[PType]) -> None:
        """Draws the next pieces in the queue"""


class RGBStyle(Style):
    """Simple RGB implementation"""
    name = "RGB"

    def __init__(self, grid: Grid, canvas: Canvas) -> None:
        super().__init__(grid)
        self.canvas = canvas
        self.init_window()
        self.next_pieces = []
        self.preview_blocks = []
        self.canvas.bind("<Configure>", self.resize, add=True)
        self.active_piece = None

    #pylint: disable=unused-argument
    def resize(self, event):
        """"Resize listener"""
        self.init_window()
        self.draw_boundaries()
        self.force_refresh()

    def init_window(self):
        """Initializes window and grid dimensions"""
        self.grid_start = (0, 0)
        self.width, self.height = (
            self.canvas.winfo_reqwidth(),
            self.canvas.winfo_reqheight(),
        )
        self.grid_stop = (int(self.width * 0.8), int(self.height))
        self.pixel_size = min(
            (self.grid_stop[0] - self.grid_start[0]) / self.grid.width,
            (self.grid_stop[1] - self.grid_start[1]) / self.grid.height,
        )
        self.grid_stop = (
            self.pixel_size * self.grid.width,
            self.pixel_size * self.grid.height,
        )

    def draw_block(self, x: int, y: int, uid, color) -> str:
        bx, by = self.coord_pixel(x, y)
        if not uid:
            uid = self.canvas.create_rectangle(
                bx, by, bx + self.pixel_size, by + self.pixel_size, fill=color
            )
            return uid
        if uid not in self.canvas.find_all():
            raise Exception(f'Block ID not found ({uid})')
        if color:
            self.canvas.itemconfig(uid, fill=color)
        self.canvas.coords(uid, bx, by, bx + self.pixel_size,
                           by + self.pixel_size)
        return uid

    def draw_piece(self, piece: Piece, active=False) -> list[Block]:
        index = 0
        blocks = []
        for x, y in piece.get_coords():
            block = Block(
                piece,
                piece.x + x,
                piece.y + y,
                self.draw_block(
                    piece.x + x,
                    piece.y + y,
                    piece.blocks[index].id if index < len(
                        piece.blocks) else None,
                    self.get_color(piece.type),
                ),
            )
            blocks.append(block)
            index += 1

        if not active:
            return blocks
        self.active_piece = piece
        o_y = piece.y
        while self.grid.try_fit(piece):
            piece.y += 1
        piece.y -= 1

        index = 0
        for x, y in piece.get_coords():
            block = Block(
                piece,
                piece.x + x,
                piece.y + y,
                self.draw_block(
                    piece.x + x,
                    piece.y + y,
                    self.preview_blocks[index].id
                    if index < len(self.preview_blocks)
                    else None,
                    self.get_color(piece.type),
                ),
            )
            # Make preview piece transparent
            self.canvas.itemconfig(block.id, stipple="gray12")
            if index >= len(self.preview_blocks):
                self.preview_blocks.append(block)
            else:
                self.preview_blocks[index] = block
            index += 1
        piece.y = o_y
        return blocks

    def draw_boundaries(self) -> None:
        item = self.canvas.find_withtag("mainbg")
        if item:
            # Change dimensions
            self.canvas.coords(item, 0, 0, self.width, self.height)
        else:
            self.canvas.create_rectangle(
                0,
                0,
                self.width,
                self.height,
                fill="#333",
                outline="#ddd",
                tags="mainbg",
            )

        item = self.canvas.find_withtag("gridbg")

        if item:
            # Change dimensions
            self.canvas.coords(
                item,
                *self.grid_start,
                self.grid_stop[0] - self.grid_start[0],
                self.grid_stop[1] - self.grid_start[1],
            )
        else:
            self.canvas.create_rectangle(
                *self.grid_start,
                self.grid_stop[0] - self.grid_start[0],
                self.grid_stop[1] - self.grid_start[1],
                fill="gray",
                tags="gridbg",
            )
        # Draw y coordinates
        for y in range(self.grid.height):
            item = self.canvas.find_withtag(f'gridtext{y}')
            tx, ty = self.grid_stop[0] + \
                15, self.grid_start[1] + y * self.pixel_size
            if item:
                self.canvas.coords(item, tx, ty)
            else:
                self.canvas.create_text(
                    self.grid_stop[0] + 15,
                    self.grid_start[1] + y * self.pixel_size,
                    text=str(y),
                    anchor="ne",
                    fill="white",
                    tags=f'gridtext{y}',
                )

    def coord_pixel(self, x, y) -> tuple[int, int]:
        return (
            x * self.pixel_size + self.grid_start[0],
            y * self.pixel_size + self.grid_start[1],
        )

    def pixel_coord(self, x, y, ignoreUnsafe=False) -> tuple[int, int]:
        if not ignoreUnsafe and self.is_oob(x, y):
            return None
        return (
            int((x - self.grid_start[0]) / self.pixel_size),
            int((y - self.grid_start[1]) / self.pixel_size),
        )

    def is_oob(self, x, y) -> bool:
        """Checks if a coordinate is out of bounds"""
        return (
            x < self.grid_start[0]
            or x > self.grid_stop[0]
            or y < self.grid_start[1]
            or y > self.grid_stop[1]
        )

    def get_color(self, ptype: PType) -> str:
        """Gets an appropriate color given a PType"""
        match ptype:
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

    def clear_lines(self) -> None:
        for block in self.grid.to_delete:
            self.canvas.delete(block.id)
        self.grid.to_delete = []
        for by in range(self.grid.height):
            for block in self.grid.blocks[by]:
                if not block:
                    continue
                self.draw_block(
                    block.x, block.y, block.id, self.get_color(
                        block.piece.type)
                )

    def clear_board(self) -> None:
        self.canvas.delete("all")
        self.next_pieces = []
        self.preview_blocks = []

    def draw_next(self, pieces: list[PType]) -> None:
        for i in range(min(len(pieces), 4)):
            next_piece = self.next_pieces[i] if i < len(
                self.next_pieces) else None
            ptype = pieces[len(pieces) - 1 - i]
            if not next_piece:
                next_piece = Piece(self.grid.width, self, ptype)
                self.next_pieces.append(next_piece)
            x, y = self.pixel_coord(
                self.grid_stop[0] + self.pixel_size * 2,
                ((i + 1) * self.pixel_size * 4),
                True,
            )
            next_piece.x = x
            next_piece.y = y
            next_piece.type = ptype
            next_piece.grid = generate_piece(next_piece.type)
            self.draw_piece(next_piece)

    def force_refresh(self) -> None:
        """"Forces objects to be refreshed, primarily used for window resizing"""
        for row in self.grid.blocks:
            for block in row:
                if not block:
                    continue
                self.canvas.delete(block.id)
                block.id = self.draw_block(
                    block.x, block.y, None, self.get_color(block.piece.type)
                )
        self.clear_lines()  # Forces the grid to refresh
        for next_piece in self.next_pieces:
            if not next_piece:
                continue
            for block in next_piece.blocks:
                if not block:
                    continue
                self.canvas.delete(block.id)
            next_piece.blocks = []
            next_piece.blocks = self.draw_piece(next_piece)
        for block in self.preview_blocks:
            self.canvas.delete(block.id)
            block.id = self.draw_block(
                block.x, block.y, None, self.get_color(block.piece.type)
            )
            self.canvas.itemconfig(block.id, stipple="gray12")
        if self.active_piece:
            self.draw_piece(self.active_piece)


class ResizingCanvas(Canvas):  # https://stackoverflow.com/a/22837522
    """A Tkinter canvas that can be resized and automatically rescales its content"""

    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        """Resize the canvas"""
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        self.scale("all", 0, 0, wscale, hscale)
