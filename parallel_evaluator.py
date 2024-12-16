
from multiprocessing import Pool
from constants import DEFAULT_PROCESS_COUNT, MIN_MOVES_FOR_PARALLEL

def evaluate_move_task(args):
    minimax_strategy, state, depth, move, maximizing = args
    next_state = state.make_move(move)
    value = minimax_strategy.alpha_beta(
        next_state,
        depth,
        float('-inf'),
        float('inf'),
        maximizing
    )
    return move, value

class ParallelEvaluator:
    def __init__(self, minimax_strategy, max_processes=DEFAULT_PROCESS_COUNT):
        self.minimax_strategy = minimax_strategy
        self.max_processes = max_processes
        self._pool = None

    def __enter__(self):
        self._pool = Pool(processes=self.max_processes)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._pool:
            self._pool.close()
            self._pool.join()

    def _evaluate_single_move(self, move, state, depth, maximizing):
        next_state = state.make_move(move)
        return self.minimax_strategy.alpha_beta(
            next_state,
            depth,
            float('-inf'),
            float('inf'),
            maximizing
        )

    def evaluate_moves(self, moves, state, depth, maximizing):
        if len(moves) < MIN_MOVES_FOR_PARALLEL:
            # For small number of moves, evaluate sequentially
            return [
                (move, self._evaluate_single_move(move, state, depth, maximizing))
                for move in moves
            ]

        # Prepare arguments for parallel processing
        task_args = [
            (self.minimax_strategy, state, depth, move, maximizing)
            for move in moves
        ]

        # Execute evaluations in parallel
        return self._pool.map(evaluate_move_task, task_args)