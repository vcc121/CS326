# chess_state.py

class ChessState:
    def __init__(self, board, turn="white"):
        self.board = board
        self.turn = turn

    def is_terminal(self):
        # For now: no moves = terminal (checkmate/stalemate later)
        return len(self.get_actions()) == 0

    def utility(self):
        piece_values = {"p":1, "n":3, "b":3, "r":5, "q":9, "k":100}
        score = 0
        # FIXED: use self.board.board instead of self.board.grid
        for row in self.board.board:
            for piece in row:
                if piece == ".":
                    continue
                value = piece_values[piece.lower()]
                if piece.isupper():
                    score += value
                else:
                    score -= value
        return score

    def get_actions(self):
        return self.board.generate_moves(self.turn)

    def result(self, move):
        new_board = self.board.copy()
        new_board.make_move(move)
        next_turn = "black" if self.turn == "white" else "white"
        return ChessState(new_board, next_turn)