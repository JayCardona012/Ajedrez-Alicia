from alicechess import Game, HumanPlayer
from alicechess.bots import RandomPlayer
from alpha_beta_bot import AlphaBetaBot

if __name__ == "__main__":
    Decision = input("Do you want to play against the computer? (y/n): ")
    if Decision == "y":
        Game(white=HumanPlayer, black=AlphaBetaBot).start_window()
    else:
        Game(white=AlphaBetaBot, black=AlphaBetaBot).start_window()

Game.new().run()