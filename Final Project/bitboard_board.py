# bitboard_board.py – full chess rules (castling, en passant, promotion)
import random as _random
from bitboard_constants import SQUARES, square_bit, count_bits, KNIGHT_ATTACKS, KING_ATTACKS, sliding_attack

# --- Zobrist hashing tables ---
_rng = _random.Random(20250428)  # fixed seed for reproducibility
_ZOBRIST_PIECES = [[_rng.getrandbits(64) for _ in range(64)] for _ in range(12)]
_ZOBRIST_SIDE = _rng.getrandbits(64)
_ZOBRIST_CASTLING = [_rng.getrandbits(64) for _ in range(16)]
_ZOBRIST_EP = [_rng.getrandbits(64) for _ in range(8)]

class Move:
    def __init__(self, start, end, piece, captured=".", promotion=None):
        self.start = start
        self.end = end
        self.piece = piece
        self.captured = captured
        self.promotion = promotion   # piece type for promotion (4=queen,1=knight,2=bishop,3=rook)
    def __repr__(self):
        return f"{self.piece}: {self.start} -> {self.end}"

class BitboardBoard:
    def __init__(self):
        self.pieces = [0] * 12
        self.occupied = [0, 0]
        self.all_occupied = 0
        self.side_to_move = 0   # 0=white,1=black
        self.castling_rights = 0b1111  # whiteK, whiteQ, blackK, blackQ
        self.en_passant_square = -1
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.setup_initial_position()

    def setup_initial_position(self):
        # Pawns
        self.pieces[0] = 0x000000000000FF00   # white pawns rank 2
        self.pieces[6] = 0x00FF000000000000   # black pawns rank 7
        # Knights
        self.pieces[1] = 0x0000000000000042   # b1, g1
        self.pieces[7] = 0x4200000000000000   # b8, g8
        # Bishops
        self.pieces[2] = 0x0000000000000024   # c1, f1
        self.pieces[8] = 0x2400000000000000   # c8, f8
        # Rooks
        self.pieces[3] = 0x0000000000000081   # a1, h1
        self.pieces[9] = 0x8100000000000000   # a8, h8
        # Queens
        self.pieces[4] = 0x0000000000000008   # d1
        self.pieces[10] = 0x0800000000000000  # d8
        # Kings
        self.pieces[5] = 0x0000000000000010   # e1
        self.pieces[11] = 0x1000000000000000  # e8
        self.update_occupancy()

    def update_occupancy(self):
        self.occupied[0] = 0
        self.occupied[1] = 0
        for i in range(12):
            if i < 6:
                self.occupied[0] |= self.pieces[i]
            else:
                self.occupied[1] |= self.pieces[i]
        self.all_occupied = self.occupied[0] | self.occupied[1]

    def copy(self):
        new = BitboardBoard()
        new.pieces = self.pieces[:]
        new.occupied = self.occupied[:]
        new.all_occupied = self.all_occupied
        new.side_to_move = self.side_to_move
        new.castling_rights = self.castling_rights
        new.en_passant_square = self.en_passant_square
        new.halfmove_clock = self.halfmove_clock
        new.fullmove_number = self.fullmove_number
        return new

    def make_move(self, move):
        start, end, piece_idx, captured_idx = move.start, move.end, move.piece, move.captured
        # Remove piece from start
        self.pieces[piece_idx] &= ~(1 << start)
        # Add piece to end
        self.pieces[piece_idx] |= (1 << end)
        # Handle capture
        if captured_idx is not None:
            self.pieces[captured_idx] &= ~(1 << end)
        # Handle en passant capture: the captured pawn is NOT on `end` but one rank behind it
        if piece_idx % 6 == 0 and end == self.en_passant_square and self.en_passant_square != -1:
            direction = 8 if piece_idx < 6 else -8
            captured_pawn_sq = end - direction
            enemy = 1 - (piece_idx // 6)
            self.pieces[enemy * 6] &= ~(1 << captured_pawn_sq)
        # Handle promotion
        if move.promotion is not None:
            # Remove pawn, add promoted piece
            self.pieces[piece_idx] &= ~(1 << end)   # remove pawn
            promoted_idx = (piece_idx // 6)*6 + move.promotion
            self.pieces[promoted_idx] |= (1 << end)
        # Update castling rights
        if piece_idx % 6 == 5:  # king
            if piece_idx < 6:   # white
                self.castling_rights &= ~0b11
            else:               # black
                self.castling_rights &= ~0b1100
        # If rook moves, remove corresponding right
        if piece_idx % 6 == 3:  # rook
            if start == 0:      # white queen rook
                self.castling_rights &= ~0b10
            elif start == 7:    # white king rook
                self.castling_rights &= ~0b01
            elif start == 56:   # black queen rook
                self.castling_rights &= ~0b1000
            elif start == 63:   # black king rook
                self.castling_rights &= ~0b0100
        # Clear en passant square
        self.en_passant_square = -1
        # Handle double pawn push -> set en passant square
        if piece_idx % 6 == 0 and abs(end - start) == 16:  # pawn double step
            self.en_passant_square = (start + end) // 2
        # Update halfmove clock
        if captured_idx is not None or piece_idx % 6 == 0:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        # Update fullmove number
        if piece_idx < 6:
            self.fullmove_number += 1
        # Switch side
        self.side_to_move ^= 1
        self.update_occupancy()

    def _is_move_plausible(self, move):
        """Quick geometric sanity check for a move (before full legality)."""
        start, end = move.start, move.end
        piece_type = move.piece % 6
        dr = end // 8 - start // 8
        dc = end % 8 - start % 8
        # Pawns
        if piece_type == 0:
            side = 0 if move.piece < 6 else 1
            direction = 1 if side == 0 else -1
            # Forward
            if dc == 0 and dr == direction:
                return True
            # Two steps
            if dc == 0 and dr == 2*direction:
                start_row = start // 8
                if (side == 0 and start_row == 1) or (side == 1 and start_row == 6):
                    return True
            # Diagonal capture
            if abs(dc) == 1 and dr == direction:
                return True
            return False
        # Knights
        if piece_type == 1:
            return (abs(dr), abs(dc)) in [(2,1), (1,2)]
        # Bishop
        if piece_type == 2:
            return abs(dr) == abs(dc)
        # Rook
        if piece_type == 3:
            return dr == 0 or dc == 0
        # Queen
        if piece_type == 4:
            return dr == 0 or dc == 0 or abs(dr) == abs(dc)
        # King
        if piece_type == 5:
            # Normal king move: 1 square in any direction.
            # Castling: king moves exactly 2 squares horizontally on its home rank.
            if max(abs(dr), abs(dc)) == 1:
                return True
            # Castling: 2 squares horizontally, no vertical movement
            if dr == 0 and abs(dc) == 2:
                return True
            return False
        return True

    def _generate_pseudo_moves(self, turn):
        moves = []
        side = 0 if turn == "white" else 1
        enemy = 1 - side
        my_pieces = self.occupied[side]
        enemy_pieces = self.occupied[enemy]

        bb = my_pieces
        while bb:
            from_sq = (bb & -bb).bit_length() - 1
            bb &= bb - 1
            piece_type = None
            for i in range(6):
                if (self.pieces[side*6 + i] >> from_sq) & 1:
                    piece_type = i
                    break
            if piece_type is None:
                continue

            if piece_type == 0:  # pawn
                direction = 8 if side == 0 else -8
                # One step forward
                to_sq = from_sq + direction
                if 0 <= to_sq < 64 and (self.all_occupied >> to_sq) & 1 == 0:
                    # Promotion?
                    if (side == 0 and to_sq // 8 == 7) or (side == 1 and to_sq // 8 == 0):
                        for prom in [4,1,2,3]:  # Q,N,B,R
                            moves.append(Move(from_sq, to_sq, side*6+piece_type, None, prom))
                    else:
                        moves.append(Move(from_sq, to_sq, side*6+piece_type, None))
                        # Two steps from start rank (only if not a promotion square)
                        start_row = from_sq // 8
                        if (side == 0 and start_row == 1) or (side == 1 and start_row == 6):
                            to_sq2 = from_sq + 2*direction
                            if 0 <= to_sq2 < 64 and (self.all_occupied >> to_sq2) & 1 == 0:
                                moves.append(Move(from_sq, to_sq2, side*6+piece_type, None))
                # Diagonal captures
                for dc in [-1, 1]:
                    to_sq = from_sq + direction + dc
                    if 0 <= to_sq < 64 and (enemy_pieces >> to_sq) & 1:
                        captured_idx = None
                        for j in range(6):
                            if (self.pieces[enemy*6 + j] >> to_sq) & 1:
                                captured_idx = enemy*6 + j
                                break
                        # Promotion on capture?
                        if (side == 0 and to_sq // 8 == 7) or (side == 1 and to_sq // 8 == 0):
                            for prom in [4,1,2,3]:
                                moves.append(Move(from_sq, to_sq, side*6+piece_type, captured_idx, prom))
                        else:
                            moves.append(Move(from_sq, to_sq, side*6+piece_type, captured_idx))

                # En passant capture
                if self.en_passant_square != -1:
                    ep_sq = self.en_passant_square
                    if abs(ep_sq % 8 - from_sq % 8) == 1 and abs(ep_sq - from_sq) in (7, 9):
                        to_sq = ep_sq
                        if (to_sq - from_sq) == direction + 1 or (to_sq - from_sq) == direction - 1:
                            captured_pawn_sq = ep_sq - direction
                            captured_idx = None
                            for j in range(6):
                                if (self.pieces[enemy*6 + j] >> captured_pawn_sq) & 1:
                                    captured_idx = enemy*6 + j
                                    break
                            if captured_idx is not None:
                                moves.append(Move(from_sq, to_sq, side*6+piece_type, captured_idx))

            elif piece_type == 1:  # knight
                attacks = KNIGHT_ATTACKS[from_sq]
                targets = attacks & ~my_pieces
                t = targets
                while t:
                    to_sq = (t & -t).bit_length() - 1
                    t &= t - 1
                    captured_idx = None
                    if (enemy_pieces >> to_sq) & 1:
                        for j in range(6):
                            if (self.pieces[enemy*6 + j] >> to_sq) & 1:
                                captured_idx = enemy*6 + j
                                break
                    moves.append(Move(from_sq, to_sq, side*6+piece_type, captured_idx))

            elif piece_type == 2 or piece_type == 3 or piece_type == 4:  # bishop, rook, queen
                piece_name = ['bishop','rook','queen'][piece_type-2]
                attacks = sliding_attack(piece_name, from_sq, self.all_occupied)
                targets = attacks & ~my_pieces
                t = targets
                while t:
                    to_sq = (t & -t).bit_length() - 1
                    t &= t - 1
                    captured_idx = None
                    if (enemy_pieces >> to_sq) & 1:
                        for j in range(6):
                            if (self.pieces[enemy*6 + j] >> to_sq) & 1:
                                captured_idx = enemy*6 + j
                                break
                    moves.append(Move(from_sq, to_sq, side*6+piece_type, captured_idx))

            elif piece_type == 5:  # king
                attacks = KING_ATTACKS[from_sq]
                targets = attacks & ~my_pieces
                t = targets
                while t:
                    to_sq = (t & -t).bit_length() - 1
                    t &= t - 1
                    captured_idx = None
                    if (enemy_pieces >> to_sq) & 1:
                        for j in range(6):
                            if (self.pieces[enemy*6 + j] >> to_sq) & 1:
                                captured_idx = enemy*6 + j
                                break
                    moves.append(Move(from_sq, to_sq, side*6+piece_type, captured_idx))

                # Castling moves
                if side == 0:  # white
                    if self.castling_rights & 0b01:  # white king side
                        if (self.all_occupied >> 5) & 1 == 0 and (self.all_occupied >> 6) & 1 == 0:
                            if not self.is_square_attacked(5, 1) and not self.is_square_attacked(6, 1):
                                moves.append(Move(4, 6, 5, None))  # e1->g1
                    if self.castling_rights & 0b10:  # white queen side
                        if (self.all_occupied >> 3) & 1 == 0 and (self.all_occupied >> 2) & 1 == 0 and (self.all_occupied >> 1) & 1 == 0:
                            if not self.is_square_attacked(3, 1) and not self.is_square_attacked(2, 1):
                                moves.append(Move(4, 2, 5, None))  # e1->c1
                else:  # black
                    if self.castling_rights & 0b0100:  # black king side
                        if (self.all_occupied >> 61) & 1 == 0 and (self.all_occupied >> 62) & 1 == 0:
                            if not self.is_square_attacked(61, 0) and not self.is_square_attacked(62, 0):
                                moves.append(Move(60, 62, 11, None))  # e8->g8
                    if self.castling_rights & 0b1000:  # black queen side
                        if (self.all_occupied >> 59) & 1 == 0 and (self.all_occupied >> 58) & 1 == 0 and (self.all_occupied >> 57) & 1 == 0:
                            if not self.is_square_attacked(59, 0) and not self.is_square_attacked(58, 0):
                                moves.append(Move(60, 58, 11, None))  # e8->c8

        return moves

    def generate_moves(self, turn):
        pseudo_moves = self._generate_pseudo_moves(turn)
        legal_moves = []
        side = 0 if turn == "white" else 1
        for move in pseudo_moves:
            # Quick geometric plausibility filter
            if not self._is_move_plausible(move):
                continue
            temp = self.copy()
            temp.make_move(move)
            if not temp.is_check(side):
                legal_moves.append(move)
        return legal_moves

    # ---------- CHECK AND ATTACK DETECTION ----------
    def is_square_attacked(self, square, side):
        from bitboard_constants import sliding_attack, KNIGHT_ATTACKS, KING_ATTACKS
        # Pawn attacks
        # A white pawn on from_sq attacks from_sq+8±1, so to find if `square`
        # is attacked by a white pawn, look for a white pawn at square-8±1.
        if side == 0:
            for dc in [-1, 1]:
                from_sq = square - 8 + dc
                if 0 <= from_sq < 64 and abs(from_sq % 8 - square % 8) == 1 and (self.pieces[0] >> from_sq) & 1:
                    return True
        else:
            # A black pawn on from_sq attacks from_sq-8±1, so look at square+8±1.
            for dc in [-1, 1]:
                from_sq = square + 8 + dc
                if 0 <= from_sq < 64 and abs(from_sq % 8 - square % 8) == 1 and (self.pieces[6] >> from_sq) & 1:
                    return True
        # Knights
        knight_attacks = KNIGHT_ATTACKS[square]
        if (side == 0 and (knight_attacks & self.pieces[1])) or (side == 1 and (knight_attacks & self.pieces[7])):
            return True
        # King
        king_attacks = KING_ATTACKS[square]
        if (side == 0 and (king_attacks & self.pieces[5])) or (side == 1 and (king_attacks & self.pieces[11])):
            return True
        # Bishops/Queens
        bishop_attacks = sliding_attack('bishop', square, self.all_occupied)
        if (side == 0 and (bishop_attacks & (self.pieces[2] | self.pieces[4]))) or (side == 1 and (bishop_attacks & (self.pieces[8] | self.pieces[10]))):
            return True
        # Rooks/Queens
        rook_attacks = sliding_attack('rook', square, self.all_occupied)
        if (side == 0 and (rook_attacks & (self.pieces[3] | self.pieces[4]))) or (side == 1 and (rook_attacks & (self.pieces[9] | self.pieces[10]))):
            return True
        return False

    def is_check(self, side):
        king_sq = None
        king_piece = 5 if side == 0 else 11
        for i in range(64):
            if (self.pieces[king_piece] >> i) & 1:
                king_sq = i
                break
        if king_sq is None:
            return False
        return self.is_square_attacked(king_sq, 1 - side)

    def print_board(self):
        symbols = ['P','N','B','R','Q','K','p','n','b','r','q','k']
        board = [['.' for _ in range(8)] for _ in range(8)]
        for i, bb in enumerate(self.pieces):
            b = bb
            while b:
                sq = (b & -b).bit_length() - 1
                r, c = divmod(sq, 8)
                board[r][c] = symbols[i]
                b &= b - 1
        print("  a b c d e f g h")
        for r in range(7, -1, -1):
            print(f"{r+1} ", end="")
            for c in range(8):
                print(f"{board[r][c]} ", end="")
            print()
        print()

    def hash(self):
        h = 0
        for i, bb in enumerate(self.pieces):
            b = bb
            while b:
                sq = (b & -b).bit_length() - 1
                b &= b - 1
                h ^= _ZOBRIST_PIECES[i][sq]
        if self.side_to_move == 1:
            h ^= _ZOBRIST_SIDE
        h ^= _ZOBRIST_CASTLING[self.castling_rights & 0xF]
        if self.en_passant_square != -1:
            h ^= _ZOBRIST_EP[self.en_passant_square % 8]
        return h