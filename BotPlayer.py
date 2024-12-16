from alicechess import Player, PromoteType

class AlphaBetaBot(Player):
    def __init__(self, color, depth: int = 3):  # Recibimos el color como argumento
        super().__init__(color)  # Pasamos el color al constructor de la clase base
        self.depth = depth  # Profundidad del árbol de búsqueda

    def make_move(self, game_state):
        """Selecciona el mejor movimiento usando Minimax con poda Alpha-Beta."""
        best_move = None
        best_value = float('-inf') if game_state.current_color == self.color else float('inf')
        
        for move in game_state.yield_player_moves():
            # Simular el movimiento
            next_state = game_state.make_move(move)
            
            # Evaluar el estado usando Minimax con poda Alpha-Beta
            move_value = self.alpha_beta(next_state, self.depth, float('-inf'), float('inf'), maximizing=(self.color == game_state.current_color))
            
            # Maximizar o minimizar dependiendo del color
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
            # Gana o pierde dependiendo del color
            return float('inf') if state.winner() == self.color else float('-inf')
        if state.is_draw():
            return 0
        
        # Heurística basada en valores de piezas
        score = 0
        piece_values = {
            "KING": 0,  # No lo incluimos en la puntuación
            "QUEEN": 9,
            "ROOK": 5,
            "BISHOP": 3,
            "KNIGHT": 3,
            "PAWN": 1
        }
        
        for piece in state.yield_all_pieces():
            value = piece_values.get(piece.type.name, 0)
            if piece.color == self.color:
                score += value
            else:
                score -= value
        
        return score

    def promote(self, game_state):
        """Selecciona la promoción como reina."""
        return PromoteType.QUEEN
