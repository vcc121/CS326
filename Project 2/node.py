class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g              # path cost so far
        self.h = h              # heuristic estimate
        self.f = g + h          # evaluation function

    def __lt__(self, other):
        # PriorityQueue / heapq will use this
        return self.f < other.f


def extract_path(node):
    path = []

    while node is not None:
        path.append(node.state)
        node = node.parent

    path.reverse()
    return path
