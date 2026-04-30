# play_game.py
from bitboard_chess_state import BitboardChessState
from search import SearchManager
from multiprocess_search import MultiprocessSearchManager
import time
import sys

# ========== GLOBAL SETTINGS ==========
DEFAULT_DEPTH = 4
USE_MULTIPROCESSING = True
NUM_PROCESSES = 4
HUMAN_PLAYS = True           # True: human plays White, AI plays Black. False: AI vs AI
SHOW_LEGAL_MOVES = False      # If True, prints all legal moves when it's human's turn
# ====================================

def square_to_name(sq):
    file = sq % 8
    rank = sq // 8 + 1
    return f"{chr(ord('a') + file)}{rank}"

def get_human_move(state):
    moves = state.get_actions()
    if SHOW_LEGAL_MOVES:
        move_map = {}
        print("Legal moves:")
        for i, move in enumerate(moves):
            start_sq = move.start
            end_sq = move.end
            start_name = square_to_name(start_sq)
            end_name = square_to_name(end_sq)
            move_str = f"{start_name}{end_name}"
            if move.promotion is not None:
                prom = ['Q','N','B','R'][move.promotion-4]
                move_str += prom
            move_map[move_str] = move
            print(f"  {i}: {move_str}")
        while True:
            cmd = input("Enter move (e.g., e2e4, e7e8q): ").strip().lower()
            if cmd in move_map:
                return move_map[cmd]
            print("Invalid move, try again.")
    else:
        while True:
            cmd = input("Enter move (e.g., e2e4, e7e8q): ").strip().lower()
            move_map = {}
            for move in moves:
                start_sq = move.start
                end_sq = move.end
                start_name = square_to_name(start_sq)
                end_name = square_to_name(end_sq)
                move_str = f"{start_name}{end_name}"
                if move.promotion is not None:
                    prom = ['Q','N','B','R'][move.promotion-4]
                    move_str += prom
                move_map[move_str] = move
            if cmd in move_map:
                return move_map[cmd]
            print("Invalid move, try again.")

def run_game(max_depth=DEFAULT_DEPTH, time_limit_ms=None):
    state = BitboardChessState(turn="white")
    print("Initial Board:")
    state.print_board()

    move_count = 0
    while not state.is_terminal():
        print(f"\n--- Move {move_count+1} ({'White' if state.turn == 'white' else 'Black'}) ---")
        # Determine if current turn should be AI
        if HUMAN_PLAYS:
            # Human plays White, AI plays Black
            ai_turn = (state.turn == 'black')
        else:
            # AI vs AI
            ai_turn = True

        if ai_turn:
            if USE_MULTIPROCESSING:
                manager = MultiprocessSearchManager(state, max_depth=max_depth,
                                                   time_limit_ms=time_limit_ms,
                                                   num_processes=NUM_PROCESSES)
            else:
                manager = SearchManager(state, max_depth=max_depth,
                                       time_limit_ms=time_limit_ms)
            print("Thinking...", end="", flush=True)
            start = time.time()
            move, score, depth, _ = manager.search()
            elapsed = (time.time() - start) * 1000
            print(f"\rAI chooses {square_to_name(move.start)}{square_to_name(move.end)} "
                  f"(score {score:.2f}, depth {depth}, time {elapsed:.1f}ms)")
            if move is None:
                print("No legal moves available. Game over.")
                break
        else:
            move = get_human_move(state)
        state = state.result(move)
        state.print_board()
        move_count += 1

    print("\n=== GAME OVER ===")
    if state.is_terminal():
        if state.board.is_check(state.board.side_to_move):
            print(f"{'White' if state.turn == 'white' else 'Black'} is checkmated!")
        else:
            print("Stalemate!")
    print(f"Total moves: {move_count}")

if __name__ == "__main__":
    depth = DEFAULT_DEPTH
    for i, arg in enumerate(sys.argv):
        if arg == "--depth" and i+1 < len(sys.argv):
            try:
                depth = int(sys.argv[i+1])
            except:
                pass
    run_game(max_depth=depth)