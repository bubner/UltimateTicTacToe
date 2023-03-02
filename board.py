# Sub game handler for tic-tac-toe
from eval import Evaluator

class Gamestates:
    PLAY = 1
    DRAW = 2
    X_WIN = 3
    O_WIN = 4

class Board:
    def __init__(self, position):
        self.position = position
        self.gamestate = Gamestates.PLAY
        self.pos = [str(x) for x in range(1, 10)]

    # Run a cycle of tic-tac-toe
    def tick(self, square, turn: bool):
        # Get the square they want and check if it's valid
        while True:
            res = input(
                f"Player {'O' if turn else 'X'} - Please choose a square\n> "
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
        if not (winner := Evaluator.who_won(self)) and Evaluator.is_board_full(self):
            self.gamestate = Gamestates.DRAW
        elif winner == "X":
            self.gamestate = Gamestates.X_WIN
        elif winner == "O":
            self.gamestate = Gamestates.O_WIN
            
            