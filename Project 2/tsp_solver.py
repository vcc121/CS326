# tsp_solver.py

import random
from tsp import (
    generate_cities,
    random_tour,
    tour_cost,
    two_opt_neighbors
)


def solve_tsp(
    num_cities,
    num_restarts,
    seed,
    coord_min=0,
    coord_max=100
):
    random_gen = random.Random(seed)

    cities = generate_cities(
        num_cities,
        random_gen,
        coord_min,
        coord_max
    )

    best_tour = None
    best_cost = float("inf")
    best_initial_cost = None
    total_iterations = 0

    for _ in range(num_restarts):

        current_tour = random_tour(num_cities, random_gen)
        current_cost = tour_cost(current_tour, cities)
        initial_cost = current_cost

        improved = True
        iterations = 0

        while improved:
            improved = False

            for neighbor in two_opt_neighbors(current_tour):
                neighbor_cost = tour_cost(neighbor, cities)

                if neighbor_cost < current_cost:
                    current_tour = neighbor
                    current_cost = neighbor_cost
                    improved = True
                    break

            iterations += 1

        total_iterations += iterations

        if current_cost < best_cost:
            best_cost = current_cost
            best_tour = current_tour
            best_initial_cost = initial_cost

    return {
        "status": "success",
        "num_cities": num_cities,
        "restarts": num_restarts,
        "cities": cities,
        "best_tour": best_tour,
        "initial_cost": best_initial_cost,
        "best_cost": best_cost,
        "iterations": total_iterations,
        "seed": seed
    }
