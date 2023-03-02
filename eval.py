# Evaluation module to determine the current gamestate

# Winning positions in a game of tic-tac-toe
winning_positions = [
    # Rows
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    # Columns
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    # Diagonals
    [1, 5, 9],
    [3, 5, 7]
]


class Evaluator:
    # Check if a board is full
    @staticmethod
    def is_board_full(board):
        return all((p == "O" or p == "X" or p == "N") for p in board.pos)

    # Check if a win or draw has occurred
    @staticmethod
    def who_won(board):
        for winpos in winning_positions:
            # Check if all the row defined in winning positions is concurrent with the board
            if all(p == "X" for p in [board.pos[int(x) - 1] for x in winpos]):
                return "X"
            elif all(p == "O" for p in [board.pos[int(x) - 1] for x in winpos]):
                # Repeat process for O squares
                return "O"
        return False
