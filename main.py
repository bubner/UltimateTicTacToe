# Implementation of ultimate tic-tac-toe
# Lucas Bubner, 2023

# Import colour functionality to the console for quality of life
from colorama import Fore
from eval import Evaluator
from board import Board


# Using an enum to store the current gamestate
class Gamestates:
    PLAY = 1
    DRAW = 2
    X_WIN = 3
    O_WIN = 4


class Players:
    Player_X = 1
    Player_O = 2


# Global board with 9 smaller boards and turn cycle variable
gpos = gamestate = None
boardnum = 0
turn_cycle = False

# Define colours for both X and O elements
COLOURS = {"X": Fore.RED, "O": Fore.BLUE}

# Get valid user input and make sure it is valid
def get_input(text):
    while True:
        res = input(text)
        if not res:
            print("Please enter a valid input.")
        else:
            return res

# Primary game tick
def gametick():
    global gpos, boardnum, gamestate, turn_cycle

    # Get target board for the player if there is no selected board
    if boardnum == 0:
        boardnum = get_input("Enter target board (1-9): ")
        
    # Get the square they want and check if it's valid
    square = get_input(f"Enter target square on board {boardnum}: ")

    # Update the board target
    gpos[int(boardnum)].tick(square)

    # Check if a (global) win or draw circumstance has happened
    if Evaluator.check_win(gpos):
        gamestate = Gamestates.X_WIN if turn_cycle else Gamestates.O_WIN
    elif Evaluator.check_draw(gpos):
        gamestate = Gamestates.DRAW

    # Update turn cycle
    turn_cycle = not turn_cycle


# Entrypoint function
def main():
    global gpos

    # Initialise a set of 9 smaller boards
    gpos = [Board(x) for x in range(1, 10)]

    while gamestate == Gamestates.PLAY:
        gametick()

    # Request rematch
    if input("Play again? [y] ") == "y":
        main()


if __name__ == "__main__":
    main()
