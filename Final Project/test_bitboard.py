from bitboard_chess_state import BitboardChessState
from search import SearchManager
import time

def run_test():
    state = BitboardChessState(turn="white")
    print("Initial Board:")
    state.print_board()

    # Search with iterative deepening, max depth 6, no time limit
    manager = SearchManager(state, max_depth=5, time_limit_ms=100000000)
    start = time.time()
    move, score, depth, nodes = manager.search()
    end = time.time()

    print("\n=== SEARCH RESULT ===")
    print(f"Best move: {move}")
    print(f"Score: {score}")
    print(f"Depth reached: {depth}")
    print(f"Nodes searched: {nodes}")
    print(f"Runtime: {(end - start)*1000:.1f} ms")

    if move:
        state = state.result(move)
        print("\nBoard After Best Move:")
        state.print_board()

if __name__ == "__main__":
    run_test()