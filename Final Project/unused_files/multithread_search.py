# multithread_search.py (refactored)
import threading
import time
import math
from alphabeta import alphabeta, SearchStats
from transposition_table import TranspositionTable
from search import SearchManager

class ParallelSearchManager:
    def __init__(self, state, max_depth=20, time_limit_ms=None, num_threads=None):
        self.state = state
        self.max_depth = max_depth
        self.time_limit_ms = time_limit_ms
        self.num_threads = num_threads or max(1, threading.active_count() - 1)
        self.tt = TranspositionTable()
        self.best_move = None
        self.best_score = -math.inf
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.stop_flag = False

    def search(self):
        threads = []
        for i in range(self.num_threads):
            # Calculate a static depth offset for this thread.
            # Offsets will be: 0, 1, 2, ..., num_threads - 1
            depth_offset = i
            t = threading.Thread(
                target=self._worker,
                args=(depth_offset,)
            )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return self.best_move, self.best_score, self.max_depth, self.tt

    def _worker(self, depth_offset):
        from bitboard_chess_state import BitboardChessState
        # Create a fresh state from a board copy
        new_board = self.state.board.copy()
        local_state = BitboardChessState(new_board, self.state.turn)
        manager = SearchManager(
            local_state,
            max_depth=self.max_depth,
            time_limit_ms=self.time_limit_ms,
            transposition_table=self.tt,
            depth_offset=depth_offset
        )
        move, score, depth_reached, nodes = manager.search()
        with self.lock:
            if score > self.best_score:
                self.best_score = score
                self.best_move = move