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

# Check if a player has won
def is_winner(board, player):
    # Check horizontally
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            if np.all(board[row, col:col+WINDOW_LENGTH] == player):
                return True

    # Check vertically
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - WINDOW_LENGTH + 1):
            if np.all(board[row:row+WINDOW_LENGTH, col] == player):
                return True

    # Check diagonally (ascending)
    for row in range(ROW_COUNT - WINDOW_LENGTH + 1):
        for col in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            if np.all(board[row:row+WINDOW_LENGTH, col:col+WINDOW_LENGTH].diagonal() == player):
                return True

    # Check diagonally (descending)
    for row in range(ROW_COUNT - WINDOW_LENGTH + 1):
        for col in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            if np.all(np.flipud(board[row:row+WINDOW_LENGTH, col:col+WINDOW_LENGTH]).diagonal() == player):
                return True

    return False
# Evaluate the current state of the board
def evaluate_board(board):
    if is_winner(board, AI):
        return 1
    elif is_winner(board, PLAYER):
        return -1
    else:
        return 0
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


# Find the best move for the AI player
def find_best_move(board):
    max_eval = float('-inf')
    best_move = None
    valid_columns = [col for col in range(COLUMN_COUNT) if is_valid_column(board, col)]
    for col in valid_columns:
        temp_board = board.copy()
        drop_disc(temp_board, col, AI)
        eval = minimax(temp_board, 4, float('-inf'), float('inf'), False)
        if eval > max_eval:
            max_eval = eval
            best_move = col
    return best_move

# Update the game board based on the player's move
def make_player_move(col):
    if is_valid_column(board, col):
        drop_disc(board, col, PLAYER)
        render_board()
        if not is_game_over(board):
            make_ai_move()

# Update the game board based on the AI's move
def make_ai_move():
    col = find_best_move(board)
    if col is not None:
        drop_disc(board, col, AI)
        render_board()
        
        
# Render the game board in the GUI
def render_board():
    for widget in game_frame.winfo_children():
        widget.destroy()
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            color = 'blue' if board[row][col] == PLAYER else 'red' if board[row][col] == AI else 'white'
            slot = tk.Canvas(game_frame, width=50, height=50, bg=color, highlightthickness=1, highlightbackground='black')
            slot.grid(row=row, column=col, padx=2, pady=2)
            slot.bind('<Button-1>', lambda e, col=col: make_player_move(col))

# Create the game board and GUI
board = create_board()
root = tk.Tk()
root.title('Connect Four')

game_frame = tk.Frame(root)
game_frame.pack()

render_board()

root.mainloop()
 
