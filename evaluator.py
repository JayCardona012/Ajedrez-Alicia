"""Game state evaluation logic."""
from constants import PIECE_VALUES

class StateEvaluator:
    def __init__(self, player_color):
        self.player_color = player_color

    def evaluate(self, state):
        """Evaluates a game state and returns a numerical score."""
        if state.is_in_checkmate():
            return float('inf') if state.winner() == self.player_color else float('-inf')
        if state.is_draw():
            return 0
        
        return self._calculate_material_score(state)
    
    def _calculate_material_score(self, state):
        """Calculates the material balance score."""
        score = 0
        for piece in state.yield_all_pieces():
            value = PIECE_VALUES.get(piece.type.name, 0)
            score += value if piece.color == self.player_color else -value
        return score