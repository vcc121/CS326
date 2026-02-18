import json
import os

from astar import astar
from grid import generate_costs
from tsp_solver import solve_tsp
from tests import (
    test_astar_start_and_goal,
    test_astar_legal_moves,
    test_astar_total_cost,
    test_tsp_valid_permutation,
    test_tsp_closed_cycle,
    test_tsp_local_minimum
)



m, n = 5, 5
start = (0, 0)
goal = (4, 4)
min_cost, max_cost = 1, 5
seed = 46

costs = generate_costs(m, n, min_cost, max_cost, seed)


def save_results(results, directory=r"C:\CS326\Project 2"):

    os.makedirs(directory, exist_ok=True)
    output_file = os.path.join(directory, "results.json")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4, sort_keys=True)

    print(f"Results saved to {output_file}")


def run_experiments():

    algorithms = {
        "astar": lambda: astar(start, goal, m, n, costs),
        "tsp": lambda: solve_tsp(
            num_cities=20,
            num_restarts=20,
            seed=seed
        )
    }

    results = []

    for name, func in algorithms.items():

        result = func()
        result["algorithm"] = name

        if "path" in result:
            result["path"] = [list(p) for p in result["path"]]

        if name == "astar":
            result.update({
                "m": m,
                "n": n,
                "start": list(start),
                "goal": list(goal),
                "min_cost": min_cost,
                "max_cost": max_cost
            })

        results.append(result)

    save_results(results)
    return results

def run_astar_tests(result):
    name = result["algorithm"]
    path = result.get("path", [])

    if result["status"] != "success":
        print(f"{name}: no path found")
        return

    if test_astar_start_and_goal(path, start, goal):
        print(f"{name}: start/goal test passed")
    else:
        print(f"{name}: start/goal test failed")

    if test_astar_legal_moves(path, m, n):
        print(f"{name}: legal moves test passed")
    else:
        print(f"{name}: legal moves test failed")

    if test_astar_total_cost(path, result["total_cost"], m, n, costs):
        print(f"{name}: total cost test passed")
    else:
        print(f"{name}: total cost test failed")

def run_tsp_tests(result, cities):
    tour = result.get("best_tour", [])
    num_cities = result["num_cities"]

    if test_tsp_valid_permutation(tour, num_cities):
        print("tsp: permutation test passed")
    else:
        print("tsp: permutation test failed")

    if test_tsp_closed_cycle(tour, num_cities):
        print("tsp: closed cycle test passed")
    else:
        print("tsp: closed cycle test failed")

    if test_tsp_local_minimum(tour, cities):
        print("tsp: local minimum test passed")
    else:
        print("tsp: local minimum test failed")

def print_astar_summary(result):
    print("A* Summary:")
    print(f"Total Cost: {result['total_cost']}")
    print(f"Steps: {result['steps']}")
    print()


def print_tsp_summary(result):
    print("TSP Summary:")
    print(f"Best Cost: {result['best_cost']}")
    print(f"Cities: {result['num_cities']}")
    print()


def run_all():

    results = run_experiments()

    print("Algorithms returned:")
    for r in results:
        print(r["algorithm"])

    print("\nAlgorithm Summaries:\n")

    for result in results:
        algo = result["algorithm"].lower()

        if algo == "astar":
            print_astar_summary(result)

        elif "tsp" in algo:
            print_tsp_summary(result)

    print("Running tests\n")

    for result in results:
        algo = result["algorithm"].lower()

        if algo == "astar":
            run_astar_tests(result)

        elif "tsp" in algo:
            run_tsp_tests(result, result["cities"])



if __name__ == "__main__":
    run_all()
