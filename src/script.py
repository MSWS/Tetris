"""Tetris game written in Python 3.10+ using tkinter for graphics."""
import tkinter as tk
from time import sleep

from game import Game
from grid import Grid
from style import ResizingCanvas, RGBStyle


def main() -> None:
    """Main entry point for the application"""
    window = tk.Tk()
    window.title("Tetris")
    grid = Grid(10, 20)
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)
    canvas = ResizingCanvas(frame, width=800, height=1000, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    style = RGBStyle(grid, canvas)

    game = Game(style, grid)
    window.bind("<Key>", game.on_key)
    canvas.addtag_all("all")

    while True:
        game.tick()
        game.render()
        window.update()
        sleep(0.01)


if __name__ == "__main__":
    main()
