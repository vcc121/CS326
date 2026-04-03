# minimax.py

def minimax(state, is_max):
    if state.is_terminal():
        return state.utility(), 1

    nodes = 1

    if is_max:
        best_value = float('-inf')

        for action in state.get_actions():
            new_state = state.result(action)
            value, child_nodes = minimax(new_state, False)

            nodes += child_nodes
            best_value = max(best_value, value)

        return best_value, nodes

    else:
        best_value = float('inf')

        for action in state.get_actions():
            new_state = state.result(action)
            value, child_nodes = minimax(new_state, True)

            nodes += child_nodes
            best_value = min(best_value, value)

        return best_value, nodes


def get_best_move(state):
    best_val = float('-inf')
    best_action = None
    total_nodes = 0

    for action in state.get_actions():
        new_state = state.result(action)
        value, nodes = minimax(new_state, False)

        total_nodes += nodes

        if value > best_val:
            best_val = value
            best_action = action

    return best_action, total_nodes