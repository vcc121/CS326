# multiprocess_search.py
import multiprocessing
import math
from search import SearchManager

class MultiprocessSearchManager:
    def __init__(self, state, max_depth=20, time_limit_ms=None, num_processes=None):
        self.state = state
        self.max_depth = max_depth
        self.time_limit_ms = time_limit_ms
        self.num_processes = num_processes or max(1, multiprocessing.cpu_count() - 1)

    def search(self):
        root_moves = list(self.state.get_actions())
        if not root_moves:
            return None, -math.inf, 0, 0

        # FIX: black minimizes, white maximizes
        maximizing = (self.state.turn == "white")

        chunks = [[] for _ in range(self.num_processes)]
        for i, move in enumerate(root_moves):
            chunks[i % self.num_processes].append(move)

        processes = []
        results = multiprocessing.Queue()
        for chunk in chunks:
            if not chunk:
                continue
            p = multiprocessing.Process(
                target=self._worker,
                args=(chunk, self.state, self.max_depth, self.time_limit_ms, maximizing, results)
            )
            p.start()
            processes.append(p)

        best_move = None
        best_score = -math.inf if maximizing else math.inf
        for _ in range(len(processes)):
            move, score = results.get()
            if maximizing and score > best_score:
                best_score = score
                best_move = move
            elif not maximizing and score < best_score:
                best_score = score
                best_move = move

        for p in processes:
            p.join()

        return best_move, best_score, self.max_depth, None

    @staticmethod
    def _worker(moves_chunk, original_state, max_depth, time_limit_ms, maximizing, result_queue):
        local_state = original_state.copy()
        best_move = None
        best_score = -math.inf if maximizing else math.inf
        for move in moves_chunk:
            new_state = local_state.result(move)
            mgr = SearchManager(new_state, max_depth=max_depth-1, time_limit_ms=time_limit_ms, verbose=False)
            _, score, _, _ = mgr.search()
            if maximizing and score > best_score:
                best_score = score
                best_move = move
            elif not maximizing and score < best_score:
                best_score = score
                best_move = move
        result_queue.put((best_move, best_score))