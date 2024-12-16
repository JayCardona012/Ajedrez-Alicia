"""Main bot class implementing the Player interface."""
from alicechess import Player, PromoteType
from evaluator import StateEvaluator
from minimax import MinimaxStrategy
from move_selector import MoveSelector
from constants import DEFAULT_THREAD_COUNT

class AlphaBetaBot(Player):
    def __init__(self, color, depth: int = 2, max_threads: int = DEFAULT_THREAD_COUNT):
        super().__init__(color)
        self.depth = depth
        
        # Initialize components
        self.evaluator = StateEvaluator(color)
        self.minimax_strategy = MinimaxStrategy(self.evaluator)
        self.move_selector = MoveSelector(self.minimax_strategy, max_threads)

    def make_move(self, game_state):
        """Selects the best move using concurrent alpha-beta search."""
        return self.move_selector.select_best_move(
            game_state,
            self.depth,
            self.color
        )

    def promote(self, game_state):
        """Selects queen for pawn promotion."""
        return PromoteType.QUEEN