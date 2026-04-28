# board.py

class Move:
    def __init__(self, start, end, piece, captured="."):
        self.start = start  # (row, col)
        self.end = end
        self.piece = piece
        self.captured = captured

    def __repr__(self):
        return f"{self.piece}: {self.start} -> {self.end}"


class Board:
    def __init__(self):
        # uppercase = white, lowercase = black
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

    def copy(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def is_white(self, piece):
        return piece.isupper()

    def is_black(self, piece):
        return piece.islower()

    def make_move(self, move):
        r1, c1 = move.start
        r2, c2 = move.end
        move.captured = self.board[r2][c2]
        self.board[r1][c1] = "."
        self.board[r2][c2] = move.piece

    def undo_move(self, move):
        r1, c1 = move.start
        r2, c2 = move.end
        self.board[r1][c1] = move.piece
        self.board[r2][c2] = move.captured

    # ---------- PIECE MOVES ----------
    def pawn_moves(self, r, c, piece):
        moves = []
        direction = -1 if piece.isupper() else 1
        # one step forward
        nr, nc = r + direction, c
        if self.in_bounds(nr, nc) and self.board[nr][nc] == ".":
            moves.append(Move((r, c), (nr, nc), piece))
            # two steps from start row
            if (piece.isupper() and r == 6) or (piece.islower() and r == 1):
                nr2 = r + 2 * direction
                if self.board[nr2][nc] == ".":
                    moves.append(Move((r, c), (nr2, nc), piece))
        # captures
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if self.in_bounds(nr, nc):
                target = self.board[nr][nc]
                if target != "." and self.is_white(piece) != self.is_white(target):
                    moves.append(Move((r, c), (nr, nc), piece))
        return moves

    def knight_moves(self, r, c, piece):
        moves = []
        offsets = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            if not self.in_bounds(nr, nc):
                continue
            target = self.board[nr][nc]
            if target == "." or self.is_white(piece) != self.is_white(target):
                moves.append(Move((r, c), (nr, nc), piece))
        return moves

    def bishop_moves(self, r, c, piece):
        moves = []
        for dr, dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            for step in range(1, 8):
                nr, nc = r + dr*step, c + dc*step
                if not self.in_bounds(nr, nc):
                    break
                target = self.board[nr][nc]
                if target == ".":
                    moves.append(Move((r, c), (nr, nc), piece))
                else:
                    if self.is_white(piece) != self.is_white(target):
                        moves.append(Move((r, c), (nr, nc), piece))
                    break
        return moves

    def rook_moves(self, r, c, piece):
        moves = []
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            for step in range(1, 8):
                nr, nc = r + dr*step, c + dc*step
                if not self.in_bounds(nr, nc):
                    break
                target = self.board[nr][nc]
                if target == ".":
                    moves.append(Move((r, c), (nr, nc), piece))
                else:
                    if self.is_white(piece) != self.is_white(target):
                        moves.append(Move((r, c), (nr, nc), piece))
                    break
        return moves

    def queen_moves(self, r, c, piece):
        return self.bishop_moves(r, c, piece) + self.rook_moves(r, c, piece)

    def king_moves(self, r, c, piece):
        moves = []
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if not self.in_bounds(nr, nc):
                    continue
                target = self.board[nr][nc]
                if target == "." or self.is_white(piece) != self.is_white(target):
                    moves.append(Move((r, c), (nr, nc), piece))
        return moves

    # ---------- GENERATE ALL LEGAL MOVES (no check validation yet) ----------
    def generate_moves(self, turn):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == ".":
                    continue
                if turn == "white" and not self.is_white(piece):
                    continue
                if turn == "black" and not self.is_black(piece):
                    continue
                p = piece.lower()
                if p == "p":
                    moves.extend(self.pawn_moves(r, c, piece))
                elif p == "n":
                    moves.extend(self.knight_moves(r, c, piece))
                elif p == "b":
                    moves.extend(self.bishop_moves(r, c, piece))
                elif p == "r":
                    moves.extend(self.rook_moves(r, c, piece))
                elif p == "q":
                    moves.extend(self.queen_moves(r, c, piece))
                elif p == "k":
                    moves.extend(self.king_moves(r, c, piece))
        return moves

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))
        print()