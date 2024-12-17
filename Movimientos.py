
from concurrent.futures import ThreadPoolExecutor, as_completed
from constants import DEFAULT_THREAD_COUNT, MIN_MOVES_FOR_PARALLEL

class MoveSelector:
    def __init__(self, minimax_strategy, max_threads=DEFAULT_THREAD_COUNT):
        self.minimax_strategy = minimax_strategy
        self.max_threads = max_threads

    def select_best_move(self, game_state, depth, player_color):
        """Selects the best move using concurrent alpha-beta search."""
        moves = list(game_state.yield_player_moves())
        
        if len(moves) <= 1:
            return moves[0] if moves else None

        return self._concurrent_move_search(moves, game_state, depth, player_color)
    
    def _concurrent_move_search(self, moves, game_state, depth, player_color):
        maximizing = game_state.current_color == player_color
        best_move = None
        best_value = float('-inf') if maximizing else float('inf')
        
        with ThreadPoolExecutor(max_workers=min(self.max_threads, len(moves))) as executor:
            future_to_move = {
                executor.submit(self._evaluate_move, move, game_state, depth, maximizing): move
                for move in moves
            }
            
            for future in as_completed(future_to_move):
                move = future_to_move[future]
                try:
                    value = future.result()
                    if self._is_better_move(value, best_value, maximizing):
                        best_value = value
                        best_move = move
                except Exception as e:
                    print(f"Error evaluating move: {e}")
                    continue
        
        return best_move
    
    def _evaluate_move(self, move, game_state, depth, maximizing):
        next_state = game_state.make_move(move)
        return self.minimax_strategy.alpha_beta(
            next_state,
            depth - 1,
            float('-inf'),
            float('inf'),
            not maximizing
        )
    
    def _is_better_move(self, move_value, best_value, maximizing):
        return (move_value > best_value) if maximizing else (move_value < best_value)