from alicechess import Game, HumanPlayer
from alicechess.bots import RandomPlayer
from alpha_beta_bot import AlphaBetaBot

if __name__ == "__main__":
    Game(white=HumanPlayer, black=AlphaBetaBot).start_window()


Game.new().run()