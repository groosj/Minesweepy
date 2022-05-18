import tkinter as tk
from minesweeperLogic import *
from tkinter.constants import BOTH
from board import *
# Python implementation of a tile for minesweeper by John Groos
# for CS321 at Carleton College Fall 2021.

class Tile(tk.Frame):

    def __init__(self, root, board, x, y, **kwargs):
        super().__init__(root, **kwargs)
        self.board = board
        self.isMine = False
        self.revealed = False
        self.flagged = False
        self.x = x
        self.y = y
        self.value = None
        self.safe = False
        self.unsafe = False
        self.previousColor = None
        self.color = "grey"

        self.pack_propagate(0)
        self.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.config(height = 32, width = 32)
        self.label = tk.Label(self)
        self.label.config(background=self.color)
        self.label.pack(fill=BOTH, expand=1)
        self.label.bind("<Button-1>", self.mouse_click)
        self.label.bind("<Button-3>", self.right_click)

    # Function which activates every mouse left click which changes the board according to which tile was clicked
    def mouse_click(self, input):
        update = self.board.updateBoard(self)
        self.update_idletasks()
        # Update is true if and only if the result of updateBoard(self) was a move which causes a change
        if update and (self.board.player == "cpu"):
            for state in self.board.relevant:
                tile = self.board.tileDict[state]
                adjTiles = self.board.getAdjacent(tile)
                addClauses(self.board, tile)
                if len(self.board.relevant) == 1:
                    for adjTile in adjTiles:
                        if adjTile.revealed:
                            addClauses(self.board, adjTile)
            self.board.relevant = []
            self.board.solveBoard()

    # Function which activates every mouse right click which changes the board according to which tile was clicked
    def right_click(self, input):
        self.board.markMine(self)
        self.update_idletasks()

    # Helper function to change current color, store the previous color, and set/display the value
    def updateTile(self, newColor, value = None):
        self.previousColor = self.color
        self.color = newColor
        self.label.config(background=newColor)
        if value != None and value != 0:
            self.value = value
            self.label.config(text = value)

    # Overload the convert to string of tile
    def __str__(self):
        if self.revealed:
            if self.isMine:
                return "X"
            else:
                return "O"
        else:
            if self.isMine:
                return "X"
            return " "
