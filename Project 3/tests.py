import sudoku
import map_coloring


# -----------------------------
# Sudoku Tests
# -----------------------------

def test_sudoku_solution(solution):
    """
    Validates a Sudoku solution according to project requirements.
    """

    if solution is None:
        return False

    # Convert solution dict to grid
    grid = [[0 for _ in range(9)] for _ in range(9)]

    for (r, c), value in solution.items():
        grid[r][c] = value

    # Check for completeness (no zeros)
    for row in grid:
        if 0 in row:
            return False

    # Check rows
    for row in grid:
        if set(row) != set(range(1, 10)):
            return False

    # Check columns
    for c in range(9):
        col = [grid[r][c] for r in range(9)]
        if set(col) != set(range(1, 10)):
            return False

    # Check 3x3 blocks
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):

            block = []

            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    block.append(grid[r][c])

            if set(block) != set(range(1, 10)):
                return False

    return True


# -----------------------------
# Map Coloring Tests
# -----------------------------

def test_map_solution(solution, neighbors):
    """
    Validates a map coloring solution according to project requirements.
    """

    if solution is None:
        return False

    # Check every region has a color
    for region in neighbors:
        if region not in solution:
            return False

    # Check adjacency constraints
    for region in neighbors:

        for neighbor in neighbors[region]:

            if solution[region] == solution[neighbor]:
                return False

    return True


# -----------------------------
# Quick test runner
# -----------------------------

def run_tests():

    print("\nRunning validation tests...\n")

    # Sudoku validation test
    sudoku_csp = sudoku.build_sudoku_csp(sudoku.instances["easy1"])
    solution, metrics = sudoku_csp.solve("mrv_fc_ac")

    if metrics["solved"]:
        valid = test_sudoku_solution(solution)
        print("Sudoku validation:", "PASS" if valid else "FAIL")
    else:
        print("Sudoku test skipped (not solved)")

    # Map validation test
    map_csp = map_coloring.build_map_csp()
    solution, metrics = map_csp.solve("mrv")

    if metrics["solved"]:
        valid = test_map_solution(solution, map_csp.neighbors)
        print("Map coloring validation:", "PASS" if valid else "FAIL")
    else:
        print("Map coloring test skipped (not solved)")

    print("\nTesting complete.\n")


if __name__ == "__main__":
    run_tests()
