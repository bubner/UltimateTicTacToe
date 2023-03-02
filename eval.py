# Evaluation module to determine the current gamestate

# Winning positions in a game of tic-tac-toe
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


class Evaluator:
    # Check if a board is full
    def is_board_full(self, board):
        return all((p == "O" or p == "X") for p in board.pos)

    # Check if a win or draw has occured
    def who_won(self, board):
        for winpos in winning_positions:
            # Check if all the row defined in winning positions is concurrent with the board
            if all(p == "X" for p in [board.pos[int(x) - 1] for x in winpos]):
                return "X"
            elif all(p == "O" for p in [board.pos[int(x) - 1] for x in winpos]):
                # Repeat process for O squares
                return "O"
        return False
