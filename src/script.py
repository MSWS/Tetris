import tkinter as tk

from grid import Grid
from style import RGBStyle


def main():
    window = tk.Tk()
    grid = Grid(10, 20)
    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()
    style = RGBStyle(grid, canvas)
    while True:
        style.drawBoundaries()
        window.update()


if __name__ == "__main__":
    main()
