from board import *
import tkinter as tk

# Python graphics implementation minesweeper by John Groos using tkinter
# for CS321 at Carleton College Fall 2021.

def main():
    size = input("S, M, or L: ")
    if (size.lower() != "s") and (size.lower() != "m") and (size.lower() != "l"):
        raise NameError('Unsuitable input')
    player = input("Would you like assistance, Y or N: ")
    if player.lower() != "y" and player.lower() != "n":
        raise NameError("That wasn't y or n :/")
    w = tk.Tk()
    if size.lower() == "s":
        width = 8
        height = 8
        numberOfMines = 10
        w.geometry("256x256")
    elif size.lower() == "m":
        width = 16
        height = 16
        numberOfMines = 40
        w.geometry("512x512")
    elif size.lower() == "l":
        width = 16
        height = 30
        numberOfMines = 99
        w.geometry("960x512")
    w.title("Mineswee.py")
    w.resizable(False, False)
    if player.lower() == "y":
        theBoard = Board(width, height, numberOfMines, w, "cpu")
    elif player.lower() == "n":
        theBoard = Board(width, height, numberOfMines, w, "human")
    theBoard.createBoard()
    w.mainloop()

main()
