from alicechess import Player, PromoteType
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class AlphaBetaBot(Player):
    def __init__(self, color, depth: int = 3, max_threads: int = 4):
        super().__init__(color)
        self.depth = depth
        self.max_threads = max_threads
        self._thread_local = threading.local()
        
        # Valores de piezas como atributo de clase para evitar recrearlos
        self.piece_values = {
            "KING": 0,  # No lo incluimos en la puntuación
            "QUEEN": 9,
            "ROOK": 5,
            "BISHOP": 3,
            "KNIGHT": 3,
            "PAWN": 1
        }

    def make_move(self, game_state):
        """Selecciona el mejor movimiento usando Minimax con poda Alpha-Beta de forma concurrente."""
        # Convertir movimientos a lista para poder iterar múltiples veces
        moves = list(game_state.yield_player_moves())
        
        # Si hay pocos movimientos, no vale la pena usar threading
        if len(moves) <= 1:
            return moves[0] if moves else None

        best_move = None
        best_value = float('-inf') if game_state.current_color == self.color else float('inf')
        
        # Usar ThreadPoolExecutor con número máximo de hilos
        with ThreadPoolExecutor(max_workers=min(self.max_threads, len(moves))) as executor:
            # Diccionario para mapear futuros a movimientos
            future_to_move = {}
            
            # Enviar trabajos al executor
            for move in moves:
                next_state = game_state.make_move(move)
                future = executor.submit(
                    self.alpha_beta, 
                    next_state, 
                    self.depth, 
                    float('-inf'), 
                    float('inf'), 
                    maximizing=(self.color == game_state.current_color)
                )
                future_to_move[future] = move
            
            # Procesar resultados a medida que se completan
            for future in as_completed(future_to_move):
                move = future_to_move[future]
                move_value = future.result()
                
                # Lógica de selección de mejor movimiento
                if (game_state.current_color == self.color and move_value > best_value) or \
                   (game_state.current_color != self.color and move_value < best_value):
                    best_value = move_value
                    best_move = move
        
        return best_move

    def alpha_beta(self, state, depth, alpha, beta, maximizing):
        """Implementa Minimax con poda Alpha-Beta."""
        if depth == 0 or state.is_game_over():
            return self.evaluate(state)
        
        if maximizing:
            max_eval = float('-inf')
            for move in state.yield_player_moves():
                next_state = state.make_move(move)
                eval = self.alpha_beta(next_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda
            return max_eval
        else:
            min_eval = float('inf')
            for move in state.yield_player_moves():
                next_state = state.make_move(move)
                eval = self.alpha_beta(next_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Poda
            return min_eval

    def evaluate(self, state):
        """Función heurística para evaluar un estado."""
        if state.is_in_checkmate():
            return float('inf') if state.winner() == self.color else float('-inf')
        if state.is_draw():
            return 0
        
        score = 0
        for piece in state.yield_all_pieces():
            value = self.piece_values.get(piece.type.name, 0)
            score += value if piece.color == self.color else -value
        
        return score

    def promote(self, game_state):
        """Selecciona la promoción como reina."""
        return PromoteType.QUEEN