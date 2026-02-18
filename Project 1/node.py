class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        
    def __lt__(self, other):
        return self.g < other.g

def extract_path(node):
    path = []

    while node is not None:
        path.append(node.state)
        node = node.parent

    path.reverse()
    return path

