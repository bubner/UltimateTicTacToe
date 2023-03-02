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


# 9 smaller boards to make up 9 smaller tic-tac-toe instances
boards = None

# Global board with final win conditions
gpos = None

# Hold the user's target board
boardnum = 0

# Determine who's turn it is
turn_cycle = False

# Define colours for both X and O elements
COLOURS = {"X": Fore.RED, "O": Fore.BLUE}


# Get valid user input and make sure it is valid
def get_input(text: str) -> int:
    while True:
        try:
            res = int(input(f"Player {'O' if turn_cycle else 'X'} - {text}"))
            if res and 1 <= res <= 9:
                return res
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid input.")


def print_gamestate():
    global gpos, gamestate, boards

    # Print the global board
    for i, x in enumerate(gpos.pos):
        print(f"{x} ", end="")
        if i % 3 == 2:
            print()

    # Print the smaller boards
    print()
    for row in range(3):
        # Print top row of each board
        for i, board in enumerate(boards[row * 3:row * 3 + 3]):
            number = row*3 + i + 1
            if i == 0 and board.gamestate == Gamestates.X_WIN:
                print(f"|__ {Fore.RED}{number}{Fore.RESET} __|", end="")
            elif i == 0 and board.gamestate == Gamestates.O_WIN:
                print(f"|__ {Fore.BLUE}{number}{Fore.RESET} __|", end="")
            else:
                print(f"|__ {number} __", end="")
        print("|", end="")
        print()
        for j in range(3):
            # Print each row of cells for each board
            for i, board in enumerate(boards[row * 3:row * 3 + 3]):
                print("| ", end="")
                for k in range(3):
                    x = board.pos[j * 3 + k]
                    print(f"{COLOURS[x] if x == 'X' or x == 'O' else ''}{x} ",
                          end="")
                    print(Fore.RESET, end="")
                if i == 2:
                    print("|", end="")
            print()
        # Print bottom row of each board
        for i, board in enumerate(boards[row * 3:row * 3 + 3]):
            if i == 0:
                print("| ----- |", end="")
            elif i == 1:
                print(" ----- ", end="")
            else:
                print("| ----- |", end="")
        print()


# Primary game tick
def gametick():
    global gpos, boardnum, turn_cycle

    # Get target board for the player if there is no selected board
    if boardnum == 0:
        boardnum = get_input("Enter target board (1-9): ")

    # Get the square they want and check if it's valid
    square = None
    while not square:
        square = get_input(f"Enter target square on board {boardnum} (1-9): ")
        # Update the board in target
        if not boards[int(boardnum) - 1].tick(square, turn_cycle):
            # Returns false if that position could not be updated
            print("You cannot place a square there!")
            square = None

    # Update the next person's turn and what board they will play on
    # If that board is full, then the player will be able to select whatever board they want
    try:
        boardnum = square if not Evaluator.is_board_full(boards[square -
                                                                1]) else 0
    except IndexError:
        # Bug with the boardnum variable where 9 is not valid and raises IndexError
        # The user input is already validated to be within 1-9 so this is a workaround
        boardnum = 9

    # Check if a (global) win or draw circumstance has happened
    if not (winner :=
            Evaluator.who_won(gpos)) and Evaluator.is_board_full(gpos):
        gpos.gamestate = Gamestates.DRAW
    elif winner == "X":
        gpos.gamestate = Gamestates.X_WIN
    elif winner == "O":
        gpos.gamestate = Gamestates.O_WIN

    # Update turn cycle
    turn_cycle = not turn_cycle

    # Print the current state of the game
    print_gamestate()


# Entrypoint function
def main():
    global gpos, gamestate, boards

    # Initialise a set of 9 smaller boards
    boards = [Board(x) for x in range(1, 10)]

    # Initialise the global board
    gpos = Board(0)

    # Print the original board
    print_gamestate()

    # Main game loop
    while gpos.gamestate == Gamestates.PLAY:
        gametick()

    # Handle final winner
    if gpos.gamestate == Gamestates.DRAW:
        print("The game is a draw!")
    elif gpos.gamestate == Gamestates.X_WIN:
        print("X wins!")
    elif gpos.gamestate == Gamestates.O_WIN:
        print("O wins!")

    # Request rematch
    if input("Play again? [y] ") == "y":
        main()


if __name__ == "__main__":
    main()
