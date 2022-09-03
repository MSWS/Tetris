from time import sleep
import tkinter as tk

from grid import Grid
from game import Game
from style import RGBStyle


def main():
    window = tk.Tk()
    window.title("Tetris")
    grid = Grid(10, 20)
    canvas = tk.Canvas(window, width=400, height=500)
    canvas.pack()
    style = RGBStyle(grid, canvas)

    game = Game(style, grid)
    window.bind("<Key>", game.onKey)

    while True:
        game.tick()
        game.render()
        window.update()
        sleep(0.01)


if __name__ == "__main__":
    main()
