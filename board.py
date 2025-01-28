import numpy as np
import random
import itertools

# Defining constants
SIZE = 3

X_CELL = 1
O_CELL = -1
EMPTY_CELL = 0

X_WIN = 1
O_WIN = -1
DRAW = 0
NOT_OVER = 2

# Making an empty board to play on
empty_board = np.full((SIZE ** 2), EMPTY_CELL)

# Play a game where each move is shown
def show_game(x_strat, o_strat):
  board = Board()
  strategies = itertools.cycle([x_strat, o_strat])

  while not board.gameover():
    play = next(strategies)
    board = play(board)
    board.print_board()

# Play a single game and return it's finished state
def play_game(x_strat, o_strat):
  board = Board()
  strategies = itertools.cycle([x_strat, o_strat])

  while not board.gameover():
    play = next(strategies)
    board = play(board)

  return board

# Generate a random move from valid indexes
def random_move(board):
  move = random.choice(board.get_valid_indexes())
  return board.play_move(move)

# Get rows and the main diagonal
def get_rows_and_diagonal(board_2d):
  return ([i for i in board_2d[range(SIZE), :]] + [board_2d.diagonal()])

# Get all rows, columns, and both diagonals to check for wins
def get_possible_wins(board_2d):
  rows_and_diagonal = get_rows_and_diagonal(board_2d)
  columns_and_diagonal = get_rows_and_diagonal(np.rot90(board_2d))
  return rows_and_diagonal + columns_and_diagonal


# ---------------------- Start of Board class ----------------------

class Board:
  # Constuctor
  def __init__(self, board=None,):
        if board is None:
            self.board = np.copy(empty_board)
        else:
            self.board = board

        self.board_2d = self.board.reshape(SIZE, SIZE)

  # Get current player turn
  def get_turn(self):
    num = np.count_nonzero(self.board)
    if (num % 2 == 0):
      return X_CELL
    else:
      return O_CELL
  
  # Get valid move indexes
  def get_valid_indexes(self):
    return np.where(self.board == EMPTY_CELL)[0]

  # Play a given valid move
  def play_move(self, move):
    new_board = np.copy(self.board)
    new_board[move] = self.get_turn()
    return Board(new_board)
    
  # Check the state of the game
  def game_result(self):
    possible_wins = get_possible_wins(self.board_2d)
    sums = list(map(sum, possible_wins))
    maximum = max(sums)
    minimum = min(sums)

    if maximum == SIZE:
      return X_WIN
    
    if minimum == -SIZE:
      return O_WIN
    
    if EMPTY_CELL not in self.board:
      return DRAW
    
    return NOT_OVER
  
  # Boolean function for gameover
  def gameover(self):
    return self.game_result() != NOT_OVER
    
  # Making a string representation of board
  def board_as_string(self):
    txt = "\n"
    for i in range(SIZE):
      pos = 0
      for j in range(SIZE):
        if (self.board_2d[i, j] == X_CELL):
          txt += "X"
        elif (self.board_2d[i, j] == O_CELL):
          txt += "O"
        else:
          txt += " "

        if ((pos % 3) == 2):
          txt += "\n"
        else:
          txt += "|"

        pos += 1

      if (i < SIZE-1):
        txt += "-----\n"
    
    return txt
        
  # Print string representation of board
  def print_board(self):
    print(self.board_as_string())

# ---------------------- End of Board class ----------------------

