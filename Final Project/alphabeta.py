# alphabeta.py – with transposition table support
import math
from transposition_table import EXACT, LOWER_BOUND, UPPER_BOUND

class SearchStats:
    def __init__(self):
        self.nodes = 0
        self.max_depth = 0

def alphabeta(state, depth, alpha, beta, maximizing, stats, current_depth=0, ordered_moves=None, tt=None):
    stats.nodes += 1
    stats.max_depth = max(stats.max_depth, current_depth)

    original_alpha = alpha

    # Probe transposition table
    if tt is not None:
        key = state.board.hash()
        entry = tt.lookup(key)
        if entry is not None:
            entry_depth, entry_value, entry_move, entry_flag = entry
            if entry_depth >= depth:
                if entry_flag == EXACT:
                    return entry_value, entry_move
                elif entry_flag == LOWER_BOUND and entry_value >= beta:
                    return entry_value, entry_move
                elif entry_flag == UPPER_BOUND and entry_value <= alpha:
                    return entry_value, None
                # TT hit with wrong bound: entry_move still useful for ordering below

    if depth <= 0 or state.is_terminal():
        score = state.utility()
        # Depth-adjust mate scores so the engine always prefers the fastest mate
        # (or longest resistance when getting mated).
        # A mate at current_depth=1 scores ±9999; at current_depth=5 it scores ±9995.
        # The engine therefore picks the shallower (quicker) mating line.
        if score >= 9000:
            score -= current_depth   # white mating: closer mate = higher score
        elif score <= -9000:
            score += current_depth   # black mating: closer mate = lower (more negative) score
        return score, None

    if ordered_moves is not None and current_depth == 0:
        moves = ordered_moves
    else:
        moves = state.get_actions()

    if not moves:
        return state.utility(), None

    best_move = None
    best_eval = -math.inf if maximizing else math.inf

    if maximizing:
        max_eval = -math.inf
        for move in moves:
            new_state = state.result(move)
            eval_score, _ = alphabeta(new_state, depth - 1, alpha, beta, False, stats, current_depth + 1, None, tt)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        best_eval = max_eval
    else:
        min_eval = math.inf
        for move in moves:
            new_state = state.result(move)
            eval_score, _ = alphabeta(new_state, depth - 1, alpha, beta, True, stats, current_depth + 1, None, tt)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        best_eval = min_eval

    # Store result in transposition table with correct node type flag
    if tt is not None:
        key = state.board.hash()
        if best_eval <= original_alpha:
            flag = UPPER_BOUND   # failed low: this is an upper bound
        elif best_eval >= beta:
            flag = LOWER_BOUND   # failed high (cut node): this is a lower bound
        else:
            flag = EXACT         # inside the window: exact minimax value
        tt.store(key, depth, best_eval, best_move, flag)

    return best_eval, best_move