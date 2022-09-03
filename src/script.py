from random import random
from time import sleep
import tkinter as tk

from grid import Grid
from game import Game
from style import RGBStyle, ResizingCanvas


def main():
    window = tk.Tk()
    window.title("Tetris")
    grid = Grid(10, 20)
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)
    canvas = ResizingCanvas(frame, width=400, height=500, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    style = RGBStyle(grid, canvas)

    game = Game(style, grid)
    window.bind("<Key>", game.onKey)
    canvas.addtag_all("all")

    while True:
        game.tick()
        game.render()
        window.update()
        sleep(0.01)


if __name__ == "__main__":
    main()
