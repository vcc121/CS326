from collections import deque
from node import Node, extract_path
from grid import succ

def bfs(start, goal, m, n, costs):
    frontier = deque()
    frontier.append(Node(start, None, None, 0))
    explored = set()

    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        node = frontier.popleft()

        # Goal test
        if node.state == goal:
            path = extract_path(node)
            return {
                "path": path,
                "steps": len(path) - 1,
                "total_cost": node.g,  # BFS ignores real costs
                "expanded": expanded,
                "generated": generated,
                "max_frontier": max_frontier,
                "status": "success"
            }

        if node.state not in explored:
            explored.add(node.state)
            expanded += 1

            for action, s2, _ in succ(node.state, m, n, costs):
                frontier.append(Node(s2, node, action, node.g + 1))
                generated += 1

    return {"status": "failure"}
