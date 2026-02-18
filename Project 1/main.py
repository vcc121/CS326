from BFS import bfs
from DFS import dfs
from UCS import ucs
from grid import generate_costs
from grid import succ
import json
import os

m, n = 5, 5      # grid size
start = (0, 0)
goal = (4, 4)
min_cost, max_cost = 1, 5
seed = 42
costs = generate_costs(m, n, min_cost, max_cost, seed)


def save_results(results, directory=r"C:\Test\CS326\Project 1"):

    os.makedirs(directory, exist_ok=True)

    output_file = os.path.join(directory, "results.json")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4, sort_keys=True)

    print(f"Results saved to {output_file}")

def run_experiments():
    algorithms = {"bfs": bfs, "dfs": dfs, "ucs": ucs}
    results = []

    for name, func in algorithms.items():
        res = func(start, goal, m, n, costs)

        if "path" in res:
            res["path"] = [list(s) for s in res["path"]]
        res.update({
            "algorithm": name,
            "m": m,
            "n": n,
            "start": list(start),
            "goal": list(goal),
            "min_cost": min_cost,
            "max_cost": max_cost,
            "seed": seed
        })

        results.append(res)

    save_results(results)
    return results

def test_start_and_goal(path):
    return path[0] == start and path[-1] == goal

def test_legal_moves(path):
    for i in range(1, len(path)):
        r1, c1 = path[i - 1]
        r2, c2 = path[i]
        dr, dc = abs(r2 - r1), abs(c2 - c1)

        if not ((dr == 1 and dc == 0) or (dr == 0 and dc == 1)):
            return False
        if not (0 <= r2 < m and 0 <= c2 < n):
            return False

    return True

def test_ucs_cost(path, total_cost):
    recomputed = 0

    for i in range(1, len(path)):
        s1 = tuple(path[i - 1])
        s2 = tuple(path[i])

        for _, next_state, cost in succ(s1, m, n, costs):
            if next_state == s2:
                recomputed += cost
                break

    return recomputed == total_cost


def run_all():  #runs test and  experiments
    results = run_experiments()

    print("\nRunning tests\n")

    for result in results:
        name = result["algorithm"]
        path = result.get("path", [])

        if result["status"] != "success":
            print(f"{name}: no path found")
            continue

        if test_start_and_goal(path):
            print(f"{name}: start and goal test passed")
        else:
            print(f"{name}: start and goal test failed")

        if test_legal_moves(path):
            print(f"{name}: legal moves test passed")
        else:
            print(f"{name}: legal moves test failed")

        if name == "ucs":
            if test_ucs_cost(path, result["total_cost"]):
                print(f"{name}: total cost test passed")
            else:
                print(f"{name}: total cost test failed")

if __name__ == "__main__":
    run_all()