# alphabeta.py – with transposition table support
import math

class SearchStats:
    def __init__(self):
        self.nodes = 0
        self.max_depth = 0

def alphabeta(state, depth, alpha, beta, maximizing, stats, current_depth=0, ordered_moves=None, tt=None):
    stats.nodes += 1
    stats.max_depth = max(stats.max_depth, current_depth)

    # Probe transposition table
    if tt is not None:
        key = state.board.hash()
        entry = tt.lookup(key)
        if entry is not None:
            entry_depth, entry_value, entry_move = entry
            if entry_depth >= depth:
                if entry_value >= beta:
                    return entry_value, entry_move
                if entry_value <= alpha:
                    return entry_value, None
                # Otherwise, we could still use entry_move for ordering, but not done here

    if depth <= 0 or state.is_terminal():
        return state.utility(), None

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

    # Store result in transposition table
    if tt is not None:
        key = state.board.hash()
        tt.store(key, depth, best_eval, best_move)

    return best_eval, best_move