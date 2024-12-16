"""Constants and configuration values for the chess bot."""

PIECE_VALUES = {
    "KING": 0,    # Not included in scoring
    "QUEEN": 9,
    "ROOK": 5,
    "BISHOP": 3,
    "KNIGHT": 3,
    "PAWN": 1
}

# Thread pool configuration
DEFAULT_THREAD_COUNT = 4
MIN_MOVES_FOR_PARALLEL = 2