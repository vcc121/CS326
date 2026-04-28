# bitboard_chess_state.py
from bitboard_board import BitboardBoard
from bitboard_constants import count_bits
from positional_tables import PIECE_TABLES

class BitboardChessState:
    def __init__(self, board=None, turn="white"):
        if board is None:
            board = BitboardBoard()
        self.board = board
        self.turn = turn

    def is_terminal(self):
        return len(self.get_actions()) == 0

    def utility(self):
        # Terminal state: checkmate or stalemate
        if self.is_terminal():
            side = 0 if self.turn == "white" else 1
            if self.board.is_check(side):
                # side to move is mated => opponent wins
                return 10000 if side == 1 else -10000
            else:
                return 0
        # Normal evaluation: material + positional
        piece_values = [1,3,3,5,9,100]
        score = 0
        for i in range(12):
            cnt = count_bits(self.board.pieces[i])
            if i < 6:
                score += cnt * piece_values[i]
            else:
                score -= cnt * piece_values[i-6]
        return score + self.positional_score()

    def positional_score(self):
        score = 0
        for side in range(2):
            for piece_type in range(6):
                idx = side*6 + piece_type
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

    def get_actions(self):
        return self.board.generate_moves(self.turn)

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