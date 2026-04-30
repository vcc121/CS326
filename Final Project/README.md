# Bitboard Chess Engine

A Python chess engine using bitboard representation and alpha-beta search with iterative deepening.

## Requirements

Python 3.10+ (requires `int.bit_count()`)

No external dependencies.

## Running

**Human vs AI**
```
python play_game.py
```

**AI vs AI**

Set `HUMAN_PLAYS = False` in `play_game.py`, then run:
```
python play_game.py
```

**Custom depth**
```
python play_game.py --depth 5
```

## Settings

At the top of `play_game.py`:

| Setting | Default | Description |
|---|---|---|
| `DEFAULT_DEPTH` | 4 | Search depth (higher = stronger but slower) |
| `HUMAN_PLAYS` | `True` | `True`: human plays White, AI plays Black |
| `USE_MULTIPROCESSING` | `True` | Parallel search across root moves |
| `NUM_PROCESSES` | 4 | Worker processes (set to your CPU core count) |
| `SHOW_LEGAL_MOVES` | `False` | Print all legal moves on your turn |

## Move Input

Enter moves in coordinate notation: `e2e4`, `g1f3`, `e7e8q` (promotion).

## Files

| File | Purpose |
|---|---|
| `play_game.py` | Entry point and game loop |
| `bitboard_board.py` | Board state and move generation |
| `bitboard_chess_state.py` | Game state wrapper and evaluation |
| `search.py` | Iterative deepening and aspiration windows |
| `alphabeta.py` | Alpha-beta search |
| `transposition_table.py` | Position cache |
| `multiprocess_search.py` | Parallel root-move search |
| `positional_tables.py` | Piece-square evaluation tables |
| `bitboard_constants.py` | Precomputed attack tables |
