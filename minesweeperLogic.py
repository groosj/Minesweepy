from board import *
from SATSolver import *
import itertools

# Python implementation of a minesweeper AI by John Groos
# for CS321 at Carleton College Fall 2021. Uses SATSolver by
# Dave Musicant.

#Function to initialize the clauses before mines are set.
def initClauses(theBoard):
    numOfStates = theBoard.columns*theBoard.rows
    listOfStates = []
    for state in range(numOfStates):
        listOfStates.append(state+1)
    theBoard.clauses.append(listOfStates)

# A function which adds new clauses to the clause list.
def addClauses(theBoard, tile):
    adjMines = tile.value
    unRevealedAdjTiles = theBoard.getAdjacentUnrevealed(tile)
    
    if len(unRevealedAdjTiles) == adjMines:
        for state in unRevealedAdjTiles:
            if [state] not in theBoard.clauses:
                theBoard.clauses.append([state])

    elif adjMines != None:
        mineCombinations = itertools.combinations(unRevealedAdjTiles, adjMines)
        for mineComb in mineCombinations:
            notMine = separate(unRevealedAdjTiles, mineComb)
            for state in notMine:
                clause = combine(mineComb, [state])
                if negate(clause) not in theBoard.clauses:
                    theBoard.clauses.append(negate(clause))
            for state in mineComb:
                clause = combine(notMine, [state])
                if clause not in theBoard.clauses:
                    theBoard.clauses.append(clause)

# Helper function designed to separate a list into two lists where one equals input
def separate(fullList, partialList):
    toReturn = []
    for element in fullList:
        if element not in partialList:
            toReturn.append(element)
    return toReturn

# Helper function designed to combine two lists/tuples
def combine(list1, list2):
    combined = []
    for element in list1:
        combined.append(element)
    for element in list2:
        combined.append(element)
    combined.sort()
    return combined

# Helper function to scale a list by -1
def negate(list):
    newList = []
    for element in list:
        newList.append(-element)
    return newList
