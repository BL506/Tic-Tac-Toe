import torch
import torch.nn as nn
import torch.nn.functional as F

import random

from collections import deque

from board import play_game
from board import random_move
from board import (X_WIN, O_WIN)

# Defining constants
BOARD_SIZE = 9

X_WIN_VALUE = 1.0
DRAW_VALUE = 0.5
O_WIN_VALUE = 0.0

# Neural Network
class TTTNet(nn.Module):
  # Constructor
  def __init__(self):
    super().__init__()

    self.input = nn.Linear(BOARD_SIZE, 18)
    self.hidden = nn.Linear(18, 18)
    self.output = nn.Linear(18, BOARD_SIZE)

  # Connecting layers forward
  def forward(self, x):
    x = self.input(x)
    x = F.relu(x)

    x = self.hidden(x)
    x = F.relu(x)

    x = self.output(x)
    return x


# Train the network againt random play
def random_train(network, total_games=100000):
  optimizer = torch.optim.SGD(network.parameters(), lr=0.01)
  loss_fn = nn.MSELoss()
  epsilon = 1
  epsilon_decay = 0.995

  # Loop for each game played
  for game in range(total_games):
    moves = deque()
    board = play_game(training_move(network, moves, epsilon), random_move)

    result = board.game_result()
    game_value = 0.5
    if result == X_WIN:
      game_value = 1
    elif result == O_WIN:
      game_value = 0

    while moves:
      board_state, move = moves.pop()
      tensor_board = torch.FloatTensor(board_state.board)
      target = network(tensor_board).detach()
      target[move] = game_value

      output = network(tensor_board)
      optimizer.zero_grad()
      loss = loss_fn(output, target)
      loss.backward()
      optimizer.step()
    
    if (game+1) % (total_games/100) == 0:
      epsilon *= epsilon_decay


# Play move chosen by NN and store board state + move index into moves
def training_move(network, moves, epsilon):
  def play(board):
    move = get_move_index(board, network, epsilon)
    moves.append((board, move))
    return board.play_move(move)
  
  return play


# Select move to play
def get_move_index(board, network, epsilon):
  valid_moves = board.get_valid_indexes()
  rand = random.random()
  if rand < epsilon:
    return random.choice(valid_moves)

  tensor_board = torch.FloatTensor(board.board)
  q_values = network(tensor_board).detach()
  valid_q_values = q_values[valid_moves]
  return valid_moves[torch.argmax(valid_q_values).item()]


# Play best move from pre-trained model
def nn_move(network, epsilon=0):
  def play(board):
    move = get_move_index(board, network, epsilon)
    return board.play_move(move)

  return play
