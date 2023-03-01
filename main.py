# Implementation of ultimate tic-tac-toe
# Lucas Bubner, 2023

# Import colour functionality to the console for quality of life
from colorama import Fore


# Using an enum to store the current gamestate
class Gamestates:
    PLAY = 1
    DRAW = 2
    X_WIN = 3
    O_WIN = 4


# Winning positions in a game of tic tac toe
winning_positions = [
    # Horizontal winning positions
    [[0, 0], [0, 1], [0, 2]],
    [[1, 0], [1, 1], [1, 2]],
    [[2, 0], [2, 1], [2, 2]],
    # Vertical winning positions
    [[0, 0], [1, 0], [2, 0]],
    [[0, 1], [1, 1], [2, 1]],
    [[0, 2], [1, 2], [2, 2]],
    # Diagonal winning positions
    [[0, 0], [1, 1], [2, 2]],
    [[0, 2], [1, 1], [2, 0]]
]

# Global board with 9 smaller boards and turn cycle variable
gpos = turn_cycle = None

# Define colours for both X and O elements
COLOURS = {"X": Fore.RED, "O": Fore.BLUE}


class Board:
    def __init__(self, position):
        self.position = position
        self.gamestate = Gamestates.PLAY
        self.pos = [str(x) for x in range(1, 10)]
        self.turn_cycle = False

    # Run a cycle of tic-tac-toe
    def tick(self):
        # Get the square they want and check if it's valid
        while True:
            res = input(
                f"Player {'O' if self.turn_cycle else 'X'} - Please choose a square\n> "
            )
            if res in [x for x in self.pos if not x == "X" or x == "O"]:
                break
            else:
                print("Please enter a valid square.")

        # Update the pos array
        if not self.turn_cycle:
            # Player X
            self.pos[int(res) - 1] = "X"
        else:
            # Player O
            self.pos[int(res) - 1] = "O"

        # Check if a win or draw circumstance has happened
        for winpos in winning_positions:
            # Check if all the row defined in winning positions is concurrent with the board
            if all(p == "X" for p in [self.pos[int(x) - 1] for x in winpos]):
                self.gamestate = Gamestates.X_WIN
                break
            elif all(p == "O" for p in [self.pos[int(x) - 1] for x in winpos]):
                # Repeat process for O squares
                self.gamestate = Gamestates.O_WIN
                break

        # Check if all spaces are occupied without a win condition
        if all((p == "O" or p == "X") for p in self.pos):
            self.gamestate = Gamestates.DRAW

        # Inverse turn_cycle for the next tick
        self.turn_cycle = not self.turn_cycle


# Primary game tick
def gametick():
    global gpos

    # Get target board for the player
    while True:
        res = input(f"Player {'O' if turn_cycle else 'X'}, enter target board (1-9)\n> ")
        if res:
            break
        else:
            print("Please enter a valid square.")

    # Select board
    gpos[int(res)].tick()


# Entrypoint function
def main():
    global gpos
    gpos = [Board(x) for x in range(1, 10)]
    gametick()

    # Request rematch
    if input("Play again? [y] ") == "y":
        main()


if __name__ == "__main__":
    main()
