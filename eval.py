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
