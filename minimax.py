"""Minimax algorithm implementation with alpha-beta pruning."""

class MinimaxStrategy:
    def __init__(self, evaluator):
        self.evaluator = evaluator

    def alpha_beta(self, state, depth, alpha, beta, maximizing):
        """Implements Minimax with alpha-beta pruning."""
        if depth == 0 or state.is_game_over():
            return self.evaluator.evaluate(state)

        if maximizing:
            return self._maximize(state, depth, alpha, beta)
        else:
            return self._minimize(state, depth, alpha, beta)
    
    def _maximize(self, state, depth, alpha, beta):
        max_eval = float('-inf')
        for move in state.yield_player_moves():
            next_state = state.make_move(move)
            eval = self.alpha_beta(next_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Pruning
        return max_eval
    
    def _minimize(self, state, depth, alpha, beta):
        min_eval = float('inf')
        for move in state.yield_player_moves():
            next_state = state.make_move(move)
            eval = self.alpha_beta(next_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Pruning
        return min_eval