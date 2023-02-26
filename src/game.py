import random

from grid import Grid
from piece import Piece, PType
from style import Style


class Game:
    """Primary Game State Instance
    Responsible for handling game controls and logic
    """

    def __init__(self, style: Style, grid: Grid) -> None:
        self.style = style
        self.grid = grid
        self.reset()
        self.pause = False
        self.bag = []
        self.fail_ticks = 0
        self.active_piece = None
        self.hold_piece = None
        self.swapped_hold = False

    def tick(self) -> None:
        """Ticks the game state, called every frame"""
        self.ticks += 1
        if self.ticks % 20 != 0 or self.pause:
            return
        if self.active_piece is None:
            self.active_piece = self.generate_piece()
            self.swapped_hold = False
            if not self.grid.try_fit(self.active_piece):
                self.reset()
            return
        self.active_piece.y += 1
        if not self.grid.try_fit(self.active_piece):
            self.active_piece.y -= 1
            self.fail_ticks += 1
            if self.fail_ticks > 3:
                self.active_piece.blocks = self.style.draw_piece(
                    self.active_piece)
                self.grid.add_piece(self.active_piece)
                self.check_clear()
                self.active_piece = None
                self.fail_ticks = 0
        else:
            self.fail_ticks = 0

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                block = self.grid.blocks[y][x]
                if not block:
                    continue
                if block.x != x or block.y != y:
                    print(f'Block at {block.x}, {block.y} is not at {x}, {y}')

    def check_clear(self) -> None:
        """Calls both grid and style clear lines which handles clearing lines"""
        self.grid.clear_lines()
        self.style.clear_lines()

    def reset(self) -> None:
        """Resets the game board, primarily meant for when the player tops out"""
        self.grid.clear()
        self.style.clear_board()
        self.active_piece = None
        self.ticks = 0
        self.fail_ticks = 0
        self.score = 0
        self.alive = True
        self.style.draw_boundaries()

    def render(self) -> None:
        """Renders the game state to the screen"""
        if self.active_piece:
            self.active_piece.blocks = self.style.draw_piece(
                self.active_piece, True)

    def generate_piece(self) -> Piece:
        """Generates the next piece to be used using the 7-bag system"""
        ptype = self.get_next_piece()
        self.style.draw_next(self.bag)
        return Piece(self.grid.width // 2 - 1, self.style, ptype)

    def get_next_piece(self) -> PType:
        """Gets the next PType to be used, does NOT generate a new Piece"""
        if len(self.bag) == 0:
            self.bag = list(PType)
            random.shuffle(self.bag)
        to_make = list(PType)
        for piece in self.bag:
            if piece in to_make:
                to_make.remove(piece)

        self.bag.insert(
            0, to_make[0] if len(to_make) > 0 else random.choice(list(PType))
        )
        return self.bag.pop()

    def on_key(self, event) -> None:
        """Input handler for the game"""
        if self.active_piece is None:
            return
        if event.keysym.lower() == "space":
            self.pause = not self.pause
            return
        if self.pause:
            return
        last_coord = (self.active_piece.x, self.active_piece.y)
        last_rotate = self.active_piece.rotation
        target_rotation = last_rotate
        match event.keysym.lower():
            case "left":
                self.active_piece.x -= 1
            case "right":
                self.active_piece.x += 1
            case "up":  # Hard drop
                while self.grid.try_fit(self.active_piece):
                    self.active_piece.y += 1
                self.active_piece.y -= 1
                self.active_piece.blocks = self.style.draw_piece(
                    self.active_piece)
                self.grid.add_piece(self.active_piece)
                self.check_clear()
                self.active_piece = None
                return
            case "down":  # Soft drop
                self.active_piece.y += 1
            case "z":
                target_rotation = (self.active_piece.rotation + 3) % 4
            case "x":
                target_rotation = (self.active_piece.rotation + 1) % 4
            case "shift_l":
                if self.swapped_hold:
                    return
                self.swapped_hold = True
                new_type = self.get_next_piece() if not self.hold_piece else self.hold_piece
                new_piece = Piece(self.grid.width // 2 -
                                  1, self.style, new_type)
                self.hold_piece = self.active_piece.type
                self.style.draw_hold(self.active_piece, self.hold_piece)
                self.active_piece = new_piece
            case "r":
                self.reset()
                return
            case _:
                print("Unknown key:", event.keysym.lower())
        if not self.grid.try_fit(self.active_piece, target_rotation):
            # Piece did not fit, revert to last position
            self.active_piece.x, self.active_piece.y = last_coord
        else:
            # Piece successfully fit, update rotation if needed
            self.active_piece.set_rotate(target_rotation)
