import heapq
from node import Node, extract_path
from grid import succ

def ucs(start, goal, m, n, costs):
    # Prio queue ordered by g(n)
    frontier = []
    heapq.heappush(frontier, Node(start, None, None, 0))

    bestCost = {}

    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        node = heapq.heappop(frontier)

        # Goal test
        if node.state == goal:
            path = extract_path(node)
            return {
                "path": path,
                "steps": len(path) - 1,
                "total_cost": node.g,   # TRUE cost for UCS
                "expanded": expanded,
                "generated": generated,
                "max_frontier": max_frontier,
                "status": "success"
            }

        # UCS expansion
        if node.state not in bestCost or node.g < bestCost[node.state]:
            bestCost[node.state] = node.g
            expanded += 1

            for action, s2, cost in succ(node.state, m, n, costs):
                child = Node(
                    s2,
                    node,
                    action,
                    node.g + cost
                )
                heapq.heappush(frontier, child)
                generated += 1

    return {"status": "failure"}
