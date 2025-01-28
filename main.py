from board import show_game
from board import random_move

from neural_network import TTTNet
from neural_network import random_train
from neural_network import nn_move

network = TTTNet()

print("Training network vs random")
random_train(network)
print("Training complete")

nn_player = nn_move(network)
count = 0

while count < 10:
  show_game(nn_player, random_move)
  count += 1
