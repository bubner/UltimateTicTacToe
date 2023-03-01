# Sub game handler for tic-tac-toe
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
        self.turn_cycle = False
        self.ownedby = None

    # Run a cycle of tic-tac-toe
    def tick(self, square):
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
                self.boardstate = Gamestates.X_WIN
                break
            elif all(p == "O" for p in [self.pos[int(x) - 1] for x in winpos]):
                # Repeat process for O squares
                self.boardstate = Gamestates.O_WIN
                break

        # Check if all spaces are occupied without a win condition
        if all((p == "O" or p == "X") for p in self.pos):
            self.boardstate = Gamestates.DRAW

        # Inverse turn_cycle for the next tick
        self.turn_cycle = not self.turn_cycle