# bitboard_constants.py (updated with sliding attacks)
import numpy as np

# Square Indices (0 = a1, 7 = h1, 8 = a2, ..., 63 = h8)
SQUARES = {
    'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7,
    'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15,
    'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23,
    'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
    'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39,
    'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47,
    'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55,
    'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63
}

def square_bit(square):
    return 1 << SQUARES[square]

def count_bits(b):
    return b.bit_count()

# Precomputed attack tables for non-sliding pieces
KNIGHT_ATTACKS = [0] * 64
KING_ATTACKS = [0] * 64

# Sliding piece ray attacks (used for magic bitboards)
BISHOP_RAYS = [[0]*64 for _ in range(64)]  # not needed; we'll use functions
ROOK_RAYS = [[0]*64 for _ in range(64)]

# For simplicity, we'll use direct ray generation without magic first.
# Magic bitboards are an optimization; we can implement later.
# For now, provide a function that generates sliding attacks given occupancy.

def sliding_attack(piece_type, square, occupied):
    """Generate attacks for bishop or rook from square with given occupancy.
       piece_type: 'bishop' or 'rook' or 'queen'
       Returns bitboard of attacked squares."""
    attacks = 0
    # Directions: bishop diagonal, rook orthogonal
    if piece_type == 'bishop':
        dirs = [(1,1), (1,-1), (-1,1), (-1,-1)]
    elif piece_type == 'rook':
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    else:  # queen
        dirs = [(1,1), (1,-1), (-1,1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]

    r = square // 8
    c = square % 8
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            target_sq = nr * 8 + nc
            attacks |= (1 << target_sq)
            if (occupied >> target_sq) & 1:
                break
            nr += dr
            nc += dc
    return attacks

# Precompute knight and king attacks
def precompute_attacks():
    # Knight
    knight_offsets = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    for square, idx in SQUARES.items():
        r = int(idx / 8)
        c = idx % 8
        attacks = 0
        for dr, dc in knight_offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                attacks |= 1 << (nr*8 + nc)
        KNIGHT_ATTACKS[idx] = attacks

    # King
    king_offsets = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    for square, idx in SQUARES.items():
        r = int(idx / 8)
        c = idx % 8
        attacks = 0
        for dr, dc in king_offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                attacks |= 1 << (nr*8 + nc)
        KING_ATTACKS[idx] = attacks

precompute_attacks()