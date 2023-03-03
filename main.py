# Implementation of ultimate tic-tac-toe
# Lucas Bubner, 2023

from os import system, name

# Play the 'computer'
from random import randint
from time import sleep

# Import colour functionality to the console for quality of life
from colorama import Fore

from board import Board
from eval import Evaluator


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

# Hold the number of moves made
moves = 0

# Setting of amount of players
players = None

# Determine who's turn it is
turn_cycle = False

# Define colours for both X and O elements
COLOURS = {"X": Fore.RED, "O": Fore.BLUE}


# Get valid user input and make sure it is valid
def get_input(text: str) -> int:
    current = "O" if turn_cycle else "X"
    while True:
        try:
            if players == 0 or (players == 1 and current == "O"):
                return randint(1, 9)
            res = int(input(f"{COLOURS[current]}Player {current}{Fore.RESET} - {text}"))
            if res and 1 <= res <= 9:
                return res
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid input.")


def print_gamestate():
    global gpos, boards

    # Clear the console depending on the OS
    system("cls" if name == "nt" else "clear")
    print()

    # Print a move count
    print(f"Move: {moves}")
    if players == 0 or (players == 1 and not turn_cycle):
        # If the computer made a move, display which one it made
        print(f"Computer played: {boardnum}")

    # Print the smaller boards
    for row in range(3):
        # Print top row of each board
        for i, board in enumerate(boards[row * 3:row * 3 + 3]):
            # If the current board is selected, print the number in green
            selected = Fore.GREEN if boardnum == board.position and gpos.gamestate == Gamestates.PLAY else ""

            # Calculate the board number
            number = row * 3 + i + 1

            if board.gamestate == Gamestates.X_WIN:
                # Update the global board with an X in the corresponding position
                gpos.pos[board.position - 1] = "X"

                # Print the board number in red if X has won that board
                print(f"{selected}|__ {Fore.RED}{number}{Fore.RESET} {selected}__{Fore.RESET}", end="")

            elif board.gamestate == Gamestates.O_WIN:
                # Update the global board with an O in the corresponding position
                gpos.pos[board.position - 1] = "O"

                # Print the board number in blue if O has won that board
                print(f"{selected}|__ {Fore.RESET}{Fore.BLUE}{number}{Fore.RESET} {selected}__{Fore.RESET}", end="")

            elif board.gamestate == Gamestates.DRAW:
                # Update the global board indicating it has tied with an N
                gpos.pos[board.position - 1] = "N"

                # Print the board number in black if the board has been drawn
                print(f"{selected}|__ {Fore.RESET}{Fore.BLACK}{number}{Fore.RESET} {selected}__{Fore.RESET}", end="")

            else:
                # Print the board number in default color if the board is still in play
                print(f"{selected}|__ {Fore.RESET}{number} {selected}__{Fore.RESET}", end="")

        print(selected + "|" + Fore.RESET)

        for j in range(3):
            # Print each row of cells for each board
            for i, board in enumerate(boards[row * 3:row * 3 + 3]):
                # If the current board is selected, print it in green
                selected = Fore.GREEN if boardnum == board.position and gpos.gamestate == Gamestates.PLAY else ""
                print(f"{selected}| {Fore.RESET}", end="")
                for k in range(3):
                    # Get the value of the current cell
                    x = board.pos[j * 3 + k]
                    # Print the cell value in color if it's X or O, else print in default color
                    print(f"{COLOURS[x] if x == 'X' or x == 'O' else ''}{x} {Fore.RESET}", end="")
                if i == 2:
                    print(f"{selected}|{Fore.RESET}", end="")
            print()

        # Print bottom row of each board
        for i, board in enumerate(boards[row * 3:row * 3 + 3]):
            # If the current board is selected, print it in green
            selected = Fore.GREEN if boardnum == board.position and gpos.gamestate == Gamestates.PLAY else ""
            if i == 0:
                print(f"{selected}| ----- |{Fore.RESET}", end="")
            elif i == 1:
                print(f" {selected}-----{Fore.RESET} ", end="")
            else:
                print(f"{selected}| ----- |{Fore.RESET}", end="")
        print()


# Primary game tick
def game_tick():
    global gpos, boardnum, turn_cycle, moves

    # Check if a (global) win or draw circumstance has happened
    if not (winner := Evaluator.who_won(gpos)) and Evaluator.is_board_full(gpos):
        gpos.gamestate = Gamestates.DRAW
        return
    elif winner == "X":
        gpos.gamestate = Gamestates.X_WIN
        return
    elif winner == "O":
        gpos.gamestate = Gamestates.O_WIN
        return

    # Get target board for the player if there is no selected board
    if boardnum == 0:
        boardnum = get_input("Select a TARGET BOARD (1-9): ")
        # Make sure the board is not full
        if Evaluator.is_board_full(boards[boardnum - 1]):
            if not (players == 0 or (players == 1 and turn_cycle)):
                # Suppress if the computer is making the decision
                print("That board is full!")
            boardnum = 0
            return
        print_gamestate()

    # Get the square they want and check if it's valid
    square = None
    while not square:
        square = get_input(f"Select a target square on {Fore.GREEN}board {boardnum}{Fore.RESET} (1-9): ")
        # Update the board in target
        if not boards[int(boardnum) - 1].tick(square, turn_cycle):
            # Returns false if that position could not be updated
            if not (players == 0 or (players == 1 and turn_cycle)):
                # Suppress if the computer is making the decision
                print("You cannot place a square there!")
            square = None

    # Update the next person's turn and what board they will play on
    # If that board is full, then the player will be able to select whatever board they want
    try:
        boardnum = square if not Evaluator.is_board_full(boards[square - 1]) else 0
    except IndexError:
        # Bug with the boardnum variable where 9 is not valid and raises IndexError
        # The user input is already validated to be within 1-9 so this is a workaround
        boardnum = 9

    moves += 1

    # Update turn cycle
    turn_cycle = not turn_cycle

    # Print the current state of the game
    print_gamestate()

    if players == 0:
        # If the game is vs the computer, wait 250ms before the computer makes its move
        sleep(0.25)


# Entrypoint function
def main():
    global gpos, boards, moves, players

    print(f"{Fore.RED}Welcome to Ultimate Tic-Tac-Toe!{Fore.RESET}")
    print("The rules are simple: get 3 in a row on any of the 9 smaller boards to win that board.")
    print("However, depending on where you place your piece, your opponent will be forced to play on a specific board.")
    print("If you force an opponent onto a full board, your opponent will be able to choose which board they play on.")
    print("The winner is who can get three in a row on the global board!")
    input(f"\n{Fore.CYAN}Press Enter to play! (or Ctrl+C to exit){Fore.RESET}\n")

    # Select options
    print(Fore.CYAN + "How many players? (0-2)" + Fore.RESET)
    print("""    0 will play the computer against itself
    1 will play against the computer
    2 will play against another player
    """)

    players = None
    while players is None:
        players = input("> ")
        if players not in ["0", "1", "2"]:
            print("Invalid input. (0-2)")
            players = None
            continue
        players = int(players)

    # Initialise a set of 9 smaller boards
    boards = [Board(x) for x in range(1, 10)]

    # Initialise the global board
    gpos = Board(0)
    moves = 0

    # Print the original board
    print_gamestate()

    # Main game loop
    while gpos.gamestate == Gamestates.PLAY:
        game_tick()

    # Handle final winner
    if gpos.gamestate == Gamestates.DRAW:
        print("\nThe game is a draw!\n")
    elif gpos.gamestate == Gamestates.X_WIN:
        print(f"\n{Fore.RED}X wins!{Fore.RESET}\n")
    elif gpos.gamestate == Gamestates.O_WIN:
        print(f"\n{Fore.BLUE}O wins!{Fore.RESET}\n")

    # Request rematch
    if input("Play again? [y] ") == "y":
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle exiting users without generating a stacktrace
        print("\nExiting...")
        exit(0)
