# Evaluation module to determine the current gamestate
from copy import deepcopy

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
        return None

    # Get all possible moves for the current board
    @staticmethod
    def get_possible_moves(board):
        return [i + 1 for i, x in enumerate(board.pos) if x != "N" and x != "X" and x != "O"]

    # Evaluate the board
    @staticmethod
    def evaluate_board(board):
        # Check if X has won
        if Evaluator.who_won(board) == "X":
            return -10
        # Check if O has won
        elif Evaluator.who_won(board) == "O":
            return 10
        # Otherwise, the game is a tie
        else:
            return 0


# !! EXPERIMENTAL ENGINE
# LIMITATIONS: Engine is not aware of winning and losing positions, and will not play optimally
#              Engine will attempt to play the same move every time when given the same board state
#              Engine will not play optimally when given a board state with a winning move
#              This is due to the fact that the engine is not designed for ultimate tic-tac-toe and does not
#              take into account the fact that the board is divided into 9 smaller boards. This can be fixed by
#              modifying how the engine evaluates the board state, but this is a complex task to do, and we have
#              resorted to using random numbers when the engine does not make a move due to its eval scope being limited
#              The engine also sometimes makes the worst possible move when given a board state with a winning move.
#              AI systems are a difficult task...
class Engine:
    def __init__(self, depth):
        self.MAX_DEPTH = depth
        self.best_move = None
        self.runs = 0

    # Run the engine
    def run(self, board, turn):
        # Reset the best move before each run
        self.best_move = None
        self.runs = 0
        # Return the best move using the Minimax algorithm with alpha-beta pruning
        self.minimax(board, self.MAX_DEPTH, turn, True, -float('inf'), float('inf'))
        return self.best_move

    def minimax(self, board, depth, turn, maximizing, alpha, beta):
        # Check if the engine has reached the maximum depth or if the game is over
        if depth == 0 or Evaluator.is_board_full(board) or Evaluator.who_won(board):
            # Return the score of the board state
            return Evaluator.evaluate_board(board)

        # Get all possible moves and save them locally
        possible_moves = Evaluator.get_possible_moves(board)

        # Check if the engine is maximizing or minimizing
        if maximizing:
            # If the engine is maximizing, set the best value to the lowest possible value
            best_value = -float('inf')
            # Loop through all possible moves
            for move in possible_moves:
                # Make the move on the hypothetical board
                new_board = deepcopy(board)
                new_board.pos[move - 1] = "O" if turn else "X"
                self.runs += 1
                # Get the minimax value for the new board using recursion
                value = self.minimax(new_board, depth - 1, not turn, False, alpha, beta)
                # Update the best value and best move
                if value > best_value:
                    best_value = value
                    self.best_move = move
                # Update alpha
                alpha = max(alpha, best_value)
                # Check if beta is less than or equal to alpha
                if beta <= alpha:
                    break
            # Return the best value
            return best_value
        else:
            # Otherwise, the engine is minimizing, and we set the best value to the highest possible value
            best_value = float('inf')
            # Loop through all possible moves
            for move in possible_moves:
                # Make the move on the hypothetical board
                new_board = deepcopy(board)
                new_board.pos[move - 1] = "O" if turn else "X"
                self.runs += 1
                # Get the minimax value for the new board using recursion
                value = self.minimax(new_board, depth - 1, not turn, True, alpha, beta)
                # Update the best value and best move
                if value < best_value:
                    best_value = value
                    self.best_move = move
                # Update beta
                beta = min(beta, best_value)
                # Check if beta is less than or equal to alpha
                if beta <= alpha:
                    break
            # Return the best value
            return best_value
