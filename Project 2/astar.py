import heapq
import time
from node import Node, extract_path
from grid import succ

def manhattan(state, goal):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def astar(start, goal, m, n, costs):
    start_time = time.perf_counter_ns()

    frontier = []
    counter = 0

    h0 = manhattan(start, goal)
    heapq.heappush(frontier, (h0, counter, Node(start, None, None, 0)))

    bestCost = {}

    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        _, _, node = heapq.heappop(frontier)

        if node.state == goal:
            path = extract_path(node)
            runtime_ms = (time.perf_counter_ns() - start_time) / 1_000_000
            return {
                "algorithm": "astar",
                "heuristic": "manhattan",
                "path": path,
                "steps": len(path) - 1,
                "total_cost": node.g,
                "expanded_states": expanded,
                "generated_nodes": generated,
                "max_frontier_size": max_frontier,
                "runtime_ms": runtime_ms,
                "status": "success"
            }

        if node.state not in bestCost or node.g < bestCost[node.state]:
            bestCost[node.state] = node.g
            expanded += 1

            for action, s2, cost in succ(node.state, m, n, costs):
                g_new = node.g + cost
                h_new = manhattan(s2, goal)
                f_new = g_new + h_new

                counter += 1
                heapq.heappush(
                    frontier,
                    (f_new, counter, Node(s2, node, action, g_new))
                )
                generated += 1

    runtime_ms = (time.perf_counter_ns() - start_time) / 1_000_000
    return {
        "algorithm": "astar",
        "heuristic": "manhattan",
        "expanded_states": expanded,
        "generated_nodes": generated,
        "max_frontier_size": max_frontier,
        "runtime_ms": runtime_ms,
        "status": "failure"
    }
