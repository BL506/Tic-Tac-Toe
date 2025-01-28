from board import show_game
from board import random_move

from neural_network import TTTNet
from neural_network import random_train

network = TTTNet()

print("Training network vs random")
random_train(network=network)
print("Training complete")


