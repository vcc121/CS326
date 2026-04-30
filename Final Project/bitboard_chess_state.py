# bitboard_chess_state.py
from bitboard_board import BitboardBoard
from bitboard_constants import count_bits
from positional_tables import PIECE_TABLES

# Scores from white's perspective.
# A large positive value means white wins; large negative means black wins.
MATE_SCORE = 10000

class BitboardChessState:
    def __init__(self, board=None, turn="white"):
        if board is None:
            board = BitboardBoard()
        self.board = board
        self.turn = turn
        self._cached_actions = None   # computed once per node, reused by is_terminal/utility

    def get_actions(self):
        """Return legal moves for the side to move, caching the result."""
        if self._cached_actions is None:
            self._cached_actions = self.board.generate_moves(self.turn)
        return self._cached_actions

    def is_terminal(self):
        """A position is terminal when the side to move has no legal moves."""
        return len(self.get_actions()) == 0

    def utility(self):
        """
        Returns a score from white's perspective:
          +MATE_SCORE  : black is checkmated (white wins)
          -MATE_SCORE  : white is checkmated (black wins)
           0           : stalemate (draw)
          otherwise    : material + positional heuristic

        Mate scores are deliberately *un-adjusted* for depth here.  The caller
        (alphabeta) subtracts `current_depth` from the magnitude so that the
        engine always prefers the *fastest* available mate.
        """
        if self.is_terminal():
            side = 0 if self.turn == "white" else 1
            if self.board.is_check(side):
                # The side to move is in checkmate — they lose.
                return -MATE_SCORE if self.turn == "white" else MATE_SCORE
            # No legal moves and not in check → stalemate.
            return 0

        return self._material_score() + self.positional_score()

    def _material_score(self):
        """Raw material count, from white's perspective."""
        piece_values = [1, 3, 3, 5, 9, 0]   # pawn/knight/bishop/rook/queen/king
        # King is excluded from material; its presence/absence is already
        # captured by checkmate detection above.
        score = 0
        for i in range(12):
            cnt = count_bits(self.board.pieces[i])
            val = piece_values[i % 6]
            score += cnt * val if i < 6 else -(cnt * val)
        return score

    def positional_score(self):
        score = 0
        for side in range(2):
            for piece_type in range(6):
                idx = side * 6 + piece_type
                bb = self.board.pieces[idx]
                table = PIECE_TABLES[piece_type]
                while bb:
                    sq = (bb & -bb).bit_length() - 1
                    bb &= bb - 1
                    if side == 0:
                        score += table[sq]
                    else:
                        mirrored_sq = (7 - (sq // 8)) * 8 + (sq % 8)
                        score -= table[mirrored_sq]
        return score

    def result(self, move):
        new_board = self.board.copy()
        new_board.make_move(move)
        next_turn = "black" if self.turn == "white" else "white"
        return BitboardChessState(new_board, next_turn)

    def print_board(self):
        self.board.print_board()

    def copy(self):
        new_board = self.board.copy()
        return BitboardChessState(new_board, self.turn)