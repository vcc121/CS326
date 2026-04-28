# bitboard_utils.py
from bitboard_constants import SQUARES

def shift_north(bitboard):
    return bitboard << 8

def shift_south(bitboard):
    return bitboard >> 8

def shift_east(bitboard):
    return (bitboard << 1) & 0xFEFEFEFEFEFEFEFE  # Mask to prevent wrapping

def shift_west(bitboard):
    return (bitboard >> 1) & 0x7F7F7F7F7F7F7F7F  # Mask to prevent wrapping

# Knight attack table (precomputed)
KNIGHT_ATTACKS = [0] * 64
def precompute_knight_attacks():
    offsets = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    for square, idx in SQUARES.items():
        for dr, dc in offsets:
            # compute target square and set bit in KNIGHT_ATTACKS[idx]