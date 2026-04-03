# alphabeta.py

def alphabeta(state, alpha, beta, is_max):
    if state.is_terminal():
        return state.utility(), 1

    nodes = 1

    if is_max:
        value = float('-inf')

        for action in state.get_actions():
            new_state = state.result(action)
            child_value, child_nodes = alphabeta(new_state, alpha, beta, False)

            nodes += child_nodes
            value = max(value, child_value)
            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value, nodes

    else:
        value = float('inf')

        for action in state.get_actions():
            new_state = state.result(action)
            child_value, child_nodes = alphabeta(new_state, alpha, beta, True)

            nodes += child_nodes
            value = min(value, child_value)
            beta = min(beta, value)

            if beta <= alpha:
                break

        return value, nodes


def get_best_move(state):
    best_val = float('-inf')
    best_action = None
    total_nodes = 0

    alpha = float('-inf')
    beta = float('inf')

    for action in state.get_actions():
        new_state = state.result(action)
        value, nodes = alphabeta(new_state, alpha, beta, False)

        total_nodes += nodes

        if value > best_val:
            best_val = value
            best_action = action

        alpha = max(alpha, best_val)

    return best_action, total_nodes