# analysis.py

import json
import random
import time
from astar import astar
from grid import generate_costs
from tsp_solver import solve_tsp

# ============================
# A* EXPERIMENTS
# ============================
def run_astar_experiments():
    grid_sizes = [10, 25, 50]  # grid sizes m = n
    seeds = list(range(10))     # 10 different seeds
    min_cost, max_cost = 1, 5
    all_results = []

    for size in grid_sizes:
        for seed in seeds:
            costs = generate_costs(size, size, min_cost, max_cost, seed)
            start = (0, 0)
            goal = (size - 1, size - 1)

            # Measure runtime
            start_time = time.perf_counter()
            result = astar(start, goal, size, size, costs)
            runtime_ms = (time.perf_counter() - start_time) * 1000
            result["runtime_ms"] = runtime_ms

            # Add metadata
            result.update({
                "algorithm": "astar",
                "m": size,
                "n": size,
                "start": list(start),
                "goal": list(goal),
                "min_cost": min_cost,
                "max_cost": max_cost,
                "heuristic": "manhattan",
                "seed": seed
            })

            # Convert path tuples to lists for JSON
            if "path" in result:
                result["path"] = [list(s) for s in result["path"]]

            all_results.append(result)

    # Save to JSON
    with open("astar_experiments.json", "w") as f:
        json.dump(all_results, f, indent=4, sort_keys=True)

    print(f"A* experiments complete: {len(all_results)} runs")
    return all_results


# ============================
# TSP EXPERIMENTS
# ============================
def run_tsp_experiments():
    problem_sizes = [20, 30, 50]
    seeds = list(range(10))
    num_restarts = 10
    all_results = []

    for n_cities in problem_sizes:
        for seed in seeds:
            # Run each restart as its own entry
            for restart_index in range(num_restarts):
                result = solve_tsp(
                    num_cities=n_cities,
                    num_restarts=1,  # one restart per call
                    seed=seed + restart_index  # ensure different tour each restart
                )

                # Only log this single restart
                single_restart_result = {
                    "algorithm": "tsp",
                    "num_cities": n_cities,
                    "seed": seed,
                    "restart_index": restart_index,
                    "cities": result["cities"],
                    "best_tour": result["best_tour"],
                    "initial_cost": result["initial_cost"],
                    "best_cost": result["best_cost"],
                    "iterations": result["iterations"]
                }

                all_results.append(single_restart_result)

    # Save to JSON
    with open("tsp_experiments.json", "w") as f:
        json.dump(all_results, f, indent=4, sort_keys=True)

    print(f"TSP experiments complete: {len(all_results)} runs")
    return all_results


if __name__ == "__main__":
    run_astar_experiments()
    run_tsp_experiments()
