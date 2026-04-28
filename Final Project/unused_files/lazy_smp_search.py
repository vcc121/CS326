# lazy_smp_search.py
import threading
import time
import math
from search import SearchManager
from transposition_table import TranspositionTable

class LazySMPManager:
    def __init__(self, state, max_depth=20, time_limit_ms=None, num_threads=4):
        self.state = state
        self.max_depth = max_depth
        self.time_limit_ms = time_limit_ms
        self.num_threads = num_threads
        self.tt = TranspositionTable()  # shared among threads
        self.best_move = None
        self.best_score = -math.inf
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.stop_flag = False

    def search(self):
        threads = []
        for i in range(self.num_threads):
            depth_offset = i  # different offset for each thread
            t = threading.Thread(target=self._worker, args=(depth_offset, i))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for t in threads:
            t.join()

        return self.best_move, self.best_score, self.max_depth, self.tt

    def _worker(self, depth_offset, thread_id):
        # Create a local state copy
        local_state = self.state.copy()
        # Only the main thread (or thread 0) should print? We'll suppress all printing.
        manager = SearchManager(
            local_state,
            max_depth=self.max_depth,
            time_limit_ms=self.time_limit_ms,
            transposition_table=self.tt,
            depth_offset=depth_offset,
            verbose=False          # no per‑thread prints
        )
        move, score, depth_reached, _ = manager.search()
        # Update global best with lock
        with self.lock:
            if score > self.best_score:
                self.best_score = score
                self.best_move = move