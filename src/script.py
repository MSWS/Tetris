import tkinter as tk

from grid import Grid
from src.game import Game
from style import RGBStyle


def main():
    window = tk.Tk()
    grid = Grid(10, 20)
    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()
    style = RGBStyle(grid, canvas)

    game = Game(style, grid)

    while True:
        game.tick()
        game.render()
        window.update()


if __name__ == "__main__":
    main()
