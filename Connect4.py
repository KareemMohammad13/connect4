import numpy as np
import tkinter as tk

# Constants
EMPTY = 0
PLAYER = 1
AI = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

# Create the game board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

# Check if a column is valid (i.e., not full)
def is_valid_column(board, col):
    return board[ROW_COUNT-1][col] == EMPTY

# Drop a disc into a column
def drop_disc(board, col, player):
    for row in range(ROW_COUNT):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return

# Check if the game is over
def is_game_over(board):
    return is_board_full(board) or is_winner(board, PLAYER) or is_winner(board, AI)

# Check if the board is full
def is_board_full(board):
    return np.all(board != EMPTY)

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_game_over(board):
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        valid_columns = [col for col in range(COLUMN_COUNT) if is_valid_column(board, col)]
        for col in valid_columns:
            temp_board = board.copy()
            drop_disc(temp_board, col, AI)
            eval = minimax(temp_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return max_eval
    else:
        min_eval = float('inf')
        valid_columns = [col for col in range(COLUMN_COUNT) if is_valid_column(board, col)]
        for col in valid_columns:
            temp_board = board.copy()
            drop_disc(temp_board, col, PLAYER)
            eval = minimax(temp_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return min_eval
