from board import Board
from chess_state import ChessState
from alphabeta import alphabeta, SearchStats

def run_test():
    board = Board()
    state = ChessState(board, turn="white")
    stats = SearchStats()

    print("Initial Board:")
    board.print_board()

    import time
    start = time.time()

    # Search depth 2 from the starting position
    score, move = alphabeta(
        state,
        depth=9,
        alpha=float("-inf"),
        beta=float("inf"),
        maximizing=True,
        stats=stats
    )

    end = time.time()

    print("\nBest Move:", move)
    print("Score:", score)
    print("\n--- SEARCH STATS ---")
    print("Nodes searched:", stats.nodes)
    print("Max depth reached:", stats.max_depth)
    print("Runtime (ms):", round((end - start) * 1000, 2))

    if move:
        board.make_move(move)

    print("\nBoard After Move:")
    board.print_board()

if __name__ == "__main__":
    run_test()