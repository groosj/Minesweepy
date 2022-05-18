from tile import *
from minesweeperLogic import *
import tkinter as tk
import random as rand
import sys
import time

# Python implementation of a minesweeper board by John Groos
# for CS321 at Carleton College Fall 2021.

class Board:
    def __init__(self, columns, rows, mines, window, player):
        self.parent = window #Tkinter window
        self.player = player #If cpu then use pycryptosat, if not then no.
        self.rows = rows #The number of rows
        self.columns = columns #The number of columns
        self.mines = mines #The number of mines
        self.revealed = 0 #Keeps track of how many tiles have been revealed
        self.firstClick = True
        self.startTime = None
        self.clauses = [] #A list of all logic clauses for the board
        self.unrevealed = [] #Keeps track of all unrevealed tiles
        self.relevant = [] #List of tiles considered relevant
        self.tileDict = {} #A dictionary to associate tiles to their state
        self.board = [] # R*C array containing all tiles
        self.lost = False

    # A Function with which creates a minesweeper board with rows*columns tiles
    # and instantiating tileDict and unrevealed
    def createBoard(self):
        initClauses(self)
        for i in range(self.rows):
            columnList = []
            for j in range(self.columns):
                xLoc = i*32
                yLoc = j*32
                tile = Tile(self.parent, self, i, j)
                tile.place(x=xLoc,y=yLoc)
                columnList.append(tile)
                self.tileDict[i*self.columns + j + 1] = tile
                self.unrevealed.append(i*self.columns + j + 1)
            self.board.append(columnList)

    # Fills the board with self.mines amount of mines
    def setMines(self, x, y):
        # UNCOMMENT NEXT LINE TO PLAY A SET SEED FOR REPEATABLE RESULTS
        # random.seed(12345)
        minesPlaced = 0
        mineChance = self.mines/(self.rows*self.columns)
        noMineXlist = [x-1, x, x+1]
        noMineYlist = [y-1, y, y+1]
        for row in range(self.rows):
            for column in range(self.columns):
                isMine = rand.randint(0,100)/100
                if mineChance > isMine and (minesPlaced < self.mines):
                    if (row not in noMineXlist) or (column not in noMineYlist):
                        relevantTile = self.board[row][column]
                        relevantTile.isMine = True
                        minesPlaced += 1
        # Only runs if not enough mines were placed during board creation
        xy = 0
        while minesPlaced < self.mines:
            xy += 1
            # Changes mine chance such that the chance to get a mine decreases every time a new mine is added
            mineChance = (self.mines-minesPlaced)/(self.rows*self.columns)
            relevantTile = self.tileDict[xy%(self.rows*self.columns) + 1]
            isMine = rand.randint(0,100)/100
            if (mineChance > isMine) and not (relevantTile.isMine):
                if (relevantTile.x not in noMineXlist) or (relevantTile.y not in noMineYlist):
                    relevantTile.isMine = True
                    minesPlaced += 1

    # Takes a tile as an input to mark it as flagged, or unflag it
    def markMine(self, tile):
        if (not tile.revealed) and (not tile.flagged):
            tile.updateTile("blue")
            tile.flagged = True
        elif tile.flagged:
            tile.updateTile(tile.previousColor)
            tile.flagged = False

    # A function which takes in a board and a tile and updates the board according
    # to what the tile is.
    def updateBoard(self, tile):
        # If the tile is already revealed don't make any updates
        if tile.revealed:
            return False
        # Make sure first click can't be a mine
        if self.firstClick:
            self.setMines(tile.x, tile.y)
            self.firstClick = False
            # print(self) #UNCOMMENT FOR BOARD
            self.startTime = time.time()
        if not tile.isMine and not tile.flagged:
            adjList = self.getAdjacent(tile)
            value = 0
            for adjTile in adjList:
                if adjTile.isMine:
                    value += 1
            tile.updateTile("tan", value)
            state = self.getKey(tile)
            if value != 0:
                self.relevant.append(state)
            tile.revealed = True
            self.unrevealed.remove(state)
            self.revealed += 1
            for adjTile in adjList:
                if (value == 0) and (not adjTile.revealed) and (not adjTile.isMine) and (not adjTile.flagged):
                    self.updateBoard(adjTile)
                elif (adjTile.value == 0) and (not adjTile.revealed) and (not adjTile.isMine) and (not adjTile.flagged):
                    self.updateBoard(adjTile)
            # If all non-mine tiles are selected win game
            if self.revealed == self.rows*self.columns - self.mines:
                self.winGame()
            return True
        # If the tile is a mine then lose game
        elif self.lost:
            tile.updateTile("red")
            return False
        elif tile.isMine and not tile.flagged:
            tile.revealed = True
            tile.updateTile("maroon", "X")
            self.loseGame()
            return False

    def revealMines(self):
        self.lost = True
        for row in self.board:
            for tile in row:
                if tile.isMine and not tile.revealed:
                    self.updateBoard(tile)
                    tile.revealed = True


    # Iterate through unrevealed tiles and then mark them safe or unsafe
    def solveBoard(self):
        for state in self.unrevealed:
            relevantTile = self.tileDict[state]
            if (not relevantTile.revealed) and (not relevantTile.unsafe) and (not relevantTile.safe):
                result = testLiteral(state, self.clauses)
                if result == True: #Is mine
                    if [state] not in self.clauses:
                        self.clauses.append([state])
                    relevantTile.updateTile("red")
                    relevantTile.unsafe = True
                elif result == False: #Not mine
                    if [-(state)] not in self.clauses:
                        self.clauses.append([-(state)])
                    relevantTile.updateTile("yellow")
                    relevantTile.safe = True

    # A function with a tile as an input and outputs a list of all adjacent tiles.
    def getAdjacent(self, tile):
        adjacentList = []
        x = tile.x
        y = tile.y
        if x - 1 >= 0:
            adjacentList.append(self.board[x-1][y])
        if x + 1 < self.rows:
            adjacentList.append(self.board[x+1][y])
        if y - 1 >= 0:
            adjacentList.append(self.board[x][y-1])
        if y + 1 < self.columns:
            adjacentList.append(self.board[x][y+1])
        if (x - 1 >= 0) and (y - 1 >= 0):
            adjacentList.append(self.board[x-1][y-1])
        if (x + 1 < self.rows) and (y - 1 >= 0):
            adjacentList.append(self.board[x+1][y-1])
        if (y + 1 < self.columns) and (x + 1 < self.rows):
            adjacentList.append(self.board[x+1][y+1])
        if (y + 1 < self.columns) and (x - 1 >= 0):
            adjacentList.append(self.board[x-1][y+1])
        return adjacentList

    # A function with a tile as an input and outputs a list of all unrevealed tiles adjacent.
    def getAdjacentUnrevealed(self, tile):
        tempAdjacentList = []
        adjacentList = []
        x = tile.x
        y = tile.y
        if x - 1 >= 0:
            tempAdjacentList.append(self.board[x-1][y])
        if x + 1 < self.rows:
            tempAdjacentList.append(self.board[x+1][y])
        if y - 1 >= 0:
            tempAdjacentList.append(self.board[x][y-1])
        if y + 1 < self.columns:
            tempAdjacentList.append(self.board[x][y+1])
        if (x - 1 >= 0) and (y - 1 >= 0):
            tempAdjacentList.append(self.board[x-1][y-1])
        if (x + 1 < self.rows) and (y - 1 >= 0):
            tempAdjacentList.append(self.board[x+1][y-1])
        if (y + 1 < self.columns) and (x + 1 < self.rows):
            tempAdjacentList.append(self.board[x+1][y+1])
        if (y + 1 < self.columns) and (x - 1 >= 0):
            tempAdjacentList.append(self.board[x-1][y+1])
        for adjTile in tempAdjacentList:
            if not adjTile.revealed:
                adjacentList.append(self.getKey(adjTile))
        return adjacentList

    # A function which retuns the state from self.tileDict from a tile
    def getKey(self, value):
        keyList = list(self.tileDict.keys())
        valList = list(self.tileDict.values())
        return(keyList[valList.index(value)])

    # End game with a loss
    def loseGame(self):
        print("YOU LOSE.")
        self.revealMines()

    # End game with a win :)
    def winGame(self):
        totalTime = (time.time() - self.startTime)
        print("YOU WIN. HUH YOU WANT A PRIZE? HOW ABOUT NO, IT TOOK YOU", (totalTime), "SECONDS.")
        sys.exit()

    # A Function that converts a Board object into a string with X rows and Y Columns
    def __str__(self):
        for i in range(self.rows + 2):
            print("_", end="")
        print()
        for row in range(self.columns):
            print("|", end="")
            for column in range(self.rows):
                print(self.board[column][row], end="")
            print("|")
        for i in range(self.rows + 2):
            print(chr(175), end="")
        return("")
