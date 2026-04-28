# search.py
import time
import math
from alphabeta import alphabeta, SearchStats
from transposition_table import TranspositionTable

class SearchManager:
    def __init__(self, state, max_depth=20, time_limit_ms=None, transposition_table=None, depth_offset=0, verbose=True):
        self.state = state
        self.max_depth = max_depth
        self.time_limit_ms = time_limit_ms
        self.tt = transposition_table if transposition_table is not None else TranspositionTable()
        self.depth_offset = depth_offset
        self.verbose = verbose
        self.start_time = 0
        self.best_move = None
        self.best_score = -math.inf
        self.previous_best_move = None
        self.previous_score = 0
        self.depth_reached = 0

        # Store root moves persistently, ordered by previous iteration's scores
        self.root_moves = list(self.state.get_actions())
        self.move_scores = {move: 0 for move in self.root_moves}

    def search(self):
        self.start_time = time.time()
        self.best_move = None
        self.best_score = -math.inf
        self.previous_best_move = None
        self.previous_score = 0

        max_eff = self.max_depth + self.depth_offset
        for eff_depth in range(1, max_eff + 1):
            if self.time_exceeded():
                if self.verbose:
                    print(f"Time exceeded at effective depth {eff_depth-1}, stopping.")
                break

            alpha = -math.inf
            beta = math.inf
            if eff_depth >= 3 and abs(self.previous_score) < 1000:
                delta = 25
                alpha = self.previous_score - delta
                beta = self.previous_score + delta

            ordered_moves = self.order_root_moves()
            stats = SearchStats()
            score, move = alphabeta(self.state, eff_depth, alpha, beta, True, stats, 0, ordered_moves, self.tt)

            if move is None:
                if self.verbose:
                    print(f"No moves found at effective depth {eff_depth}")
                break

            if score <= alpha:
                if self.verbose:
                    print(f"Fail low at depth {eff_depth} (score {score} <= {alpha}), re-searching full window")
                stats = SearchStats()
                score, move = alphabeta(self.state, eff_depth, -math.inf, math.inf, True, stats, 0, ordered_moves, self.tt)
            elif score >= beta:
                if self.verbose:
                    print(f"Fail high at depth {eff_depth} (score {score} >= {beta}), re-searching full window")
                stats = SearchStats()
                score, move = alphabeta(self.state, eff_depth, -math.inf, math.inf, True, stats, 0, ordered_moves, self.tt)

            self.move_scores[move] = score
            self.root_moves = ordered_moves
            self.best_move = move
            self.best_score = score
            self.previous_score = score
            self.previous_best_move = move
            self.depth_reached = eff_depth - self.depth_offset

            elapsed = (time.time() - self.start_time) * 1000
            if self.verbose:
                print(f"Depth {eff_depth}: best move {move}, score {score}, nodes {stats.nodes}, time {elapsed:.1f} ms")

            if abs(score) >= 10000:
                if self.verbose:
                    print(f"Forced mate found, stopping.")
                break

        return self.best_move, self.best_score, self.depth_reached, self.tt

    def order_root_moves(self):
        def move_key(move):
            return self.move_scores.get(move, -math.inf)
        return sorted(self.root_moves, key=move_key, reverse=True)

    def time_exceeded(self):
        if self.time_limit_ms is None:
            return False
        return (time.time() - self.start_time) * 1000 >= self.time_limit_ms