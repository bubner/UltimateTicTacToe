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
    def tick(self, square: int, turn: bool) -> bool:
        if self.pos[square - 1] in ["X", "O"]:
            return False
        
        # Update the pos array
        if not turn:
            # Player X
            self.pos[square - 1] = "X"
        else:
            # Player O
            self.pos[square - 1] = "O"

        # Check if a win or draw circumstance has happened
        if not (winner := Evaluator.who_won(self)) and Evaluator.is_board_full(self):
            self.gamestate = Gamestates.DRAW
        elif winner == "X":
            self.gamestate = Gamestates.X_WIN
        elif winner == "O":
            self.gamestate = Gamestates.O_WIN

        return True
