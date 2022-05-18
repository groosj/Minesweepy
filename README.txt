Welcome to my python3 implementation of minesweeper. To run you need python3 with
tkinter, pycryptosat, and a screen environment to display on (for windows can use Xming (VcXsrv)),
for mac and linux it uses the normal screen. To ssh to mirage with a windows Xming (VcXsrv) is
needed and then follow these instructions: https://wiki.carleton.edu/display/carl/How+to+use+X+Session+Forwarding+on+Windows

To work "board.py", "displayMinesweeper.py", "tile.py", "mineswee.py", "SATSolver", and minesweeperLogic.py
must all be in the same folder.

To play the game cd to the folder containing all the files and type python3 playMinesweeper.py
Then when prompted for input simply type S, M, or L (lowercase is fine too).

For the next line of input, if you wish to play where the computer uses pycryptosat to solve the board
and use logic to display safe and unsafe tiles simply type Y (lowercase is fine). Else type N (lowercase is fine).

While playing, left clicking a tile reveals it and right clicking a tile marks
it as "flagged" and changes its color to blue, while making it so that it cannot be selected.
To win every tile that isn't a mine needs to be selected, regardless of whether every tile which is a mine is flagged.

If help was selected then the board will display yellow tiles which are unrevealed tiles which are known to be safe
using all available logic shown to the board. It will do the same with tiles which are solved to be mines with red tiles.
Any tile which is grey has some odds of being a mine.

If you wish to see a copy of the board with all mines shown, uncomment line 88 in board.py.

Hope you enjoy, this was a lot of fun to make.

- John C Groos
