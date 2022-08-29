import pty
import tkinter as tk

import piece as piece


def main():
    for p in piece.PType:
        print(p)
        temp = piece.Piece(p)
        print(temp.getCoords())
    print("done")
    # window = tk.Tk()
    # greeting = tk.Label(text="Hello, World!")
    # greeting.pack()
    # window.mainloop()


if __name__ == "__main__":
    main()
