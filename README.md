# Mineswee.py
Python implementation of Minesweeper using Tkinter and a Satisfiability (SAT) Solver.

Welcome to my python3 implementation of minesweeper. To run you need python3 with
tkinter, pycryptosat, and a screen environment to display on. (For windows you can use VcXsrv)
https://pypi.org/project/pycryptosat/

To work "board.py", "tile.py", "mineswee.py", "SATSolver.py", and "minesweeperLogic.py" must all be in the same folder. Thank you to Professor Dave Musicant for the "SATSolver.py" file. 

Play the game by running "python3 mineswee.py" in Terminal and responding to the prompts given in the command line.
The first line will ask you for the size of board wanted, and options are S (small), M (medium), and L (large).
For the next line of input, if you wish to play where the computer uses pycryptosat to solve the board to display safe and unsafe tiles simply type Y . Else type N.
Any inputs can be lowercase or uppercase and will still be valid.

While playing, left clicking a tile reveals it and right clicking a tile marks it as "flagged" and changes its color to blue, making the tile unselectable. To undo a flag right click again on that tile. To win every tile that isn't a mine needs to be selected, regardless of whether every tile which is a mine is flagged.

If help was selected then the board will display yellow tiles which are unrevealed tiles which are known to be safe using all available logic shown to the board. Tiles that are red are unrevealed tiles which are mines. Any tile which is grey has some odds of being a mine.

If you wish to see a copy of the board with all mines shown, uncomment line 92 in board.py.

Hope you enjoy, this was a lot of fun to make.

-John C Groos
