import random
from node import Node, extract_path

# A state is (row, col)
# Grid size is m x n
# r, c = row, col



def succ(state, m, n, costs):
    r, c = state
    successors = []

    moves = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }

    for action, (dr, dc) in moves.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n:
            cost = costs[(state, (nr, nc))]
            successors.append((action, (nr, nc), cost))

    return successors

def generate_costs(m, n, min_cost, max_cost, seed):
    random.seed(seed)
    costs = {}

    # dr and cr represent the offset from r and c
    # nr and cr represent the row and col you have moved to
    # nr = r + dr, nc = c + dc
    

    for r in range(m):
        for c in range(n):
            for action, (dr, dc) in {
                "UP": (-1, 0),
                "DOWN": (1, 0),
                "LEFT": (0, -1),
                "RIGHT": (0, 1)
            }.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    costs[((r, c), (nr, nc))] = random.randint(min_cost, max_cost)

    return costs