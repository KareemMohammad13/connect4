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
