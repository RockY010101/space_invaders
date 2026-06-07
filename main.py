import sys
import os

# Ensure the project directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
