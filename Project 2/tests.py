# tests.py

from grid import succ
from tsp import two_opt_neighbors, tour_cost


# =====================================================
# A* TESTS
# =====================================================

def test_astar_start_and_goal(path, start, goal):
    if not path:
        return False

    start_state = tuple(path[0])
    goal_state = tuple(path[-1])

    return start_state == start and goal_state == goal



def test_astar_legal_moves(path, m, n):
    """
    Check that each move is:
    - exactly one step up/down/left/right
    - remains within grid bounds
    """
    if not path:
        return False

    for i in range(1, len(path)):
        r1, c1 = path[i - 1]
        r2, c2 = path[i]

        dr = abs(r2 - r1)
        dc = abs(c2 - c1)

        # must move exactly one grid cell
        if not ((dr == 1 and dc == 0) or (dr == 0 and dc == 1)):
            return False

        # must stay in bounds
        if not (0 <= r2 < m and 0 <= c2 < n):
            return False

    return True


def test_astar_total_cost(path, reported_cost, m, n, costs):
    """
    Recompute total cost of returned path and compare.
    """
    if not path:
        return False

    recomputed = 0

    for i in range(1, len(path)):
        s1 = tuple(path[i - 1])
        s2 = tuple(path[i])

        found = False

        for _, next_state, cost in succ(s1, m, n, costs):
            if next_state == s2:
                recomputed += cost
                found = True
                break

        if not found:
            return False

    return recomputed == reported_cost


# =====================================================
# TSP TESTS
# =====================================================

def test_tsp_valid_permutation(tour, num_cities):
    """
    Verify each city appears exactly once.
    """
    if not tour:
        return False

    return sorted(tour) == list(range(num_cities))


def test_tsp_closed_cycle(tour, num_cities):
    """
    Ensure tour length matches number of cities.
    (Closed cycle is enforced by cost function.)
    """
    if not tour:
        return False

    return len(tour) == num_cities


def test_tsp_local_minimum(tour, cities):
    """
    Verify no improving 2-opt neighbor exists.
    Confirms hill climbing terminated properly.
    """
    if not tour:
        return False

    current_cost = tour_cost(tour, cities)

    for neighbor in two_opt_neighbors(tour):
        if tour_cost(neighbor, cities) < current_cost:
            return False

    return True
