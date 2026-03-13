from csp_solver import CSP

# 6 Sudoku puzzles (0 = blank)
instances = {
    "easy1": [
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],
        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],
        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9]
    ],
    "easy2": [
        [8,0,0, 0,0,0, 0,0,0],
        [0,0,3, 6,0,0, 0,0,0],
        [0,7,0, 0,9,0, 2,0,0],
        [0,5,0, 0,0,7, 0,0,0],
        [0,0,0, 0,4,5, 7,0,0],
        [0,0,0, 1,0,0, 0,3,0],
        [0,0,1, 0,0,0, 0,6,8],
        [0,0,8, 5,0,0, 0,1,0],
        [0,9,0, 0,0,0, 4,0,0]
    ],
    "med1": [
        [1,0,0, 0,0,7, 0,9,0],
        [0,3,0, 0,2,0, 0,0,8],
        [0,0,9, 6,0,0, 5,0,0],
        [0,0,5, 3,0,0, 9,0,0],
        [0,1,0, 0,8,0, 0,0,2],
        [6,0,0, 0,0,4, 0,0,0],
        [3,0,0, 0,0,0, 0,1,0],
        [0,4,1, 0,0,0, 0,0,7],
        [0,0,7, 0,0,0, 3,0,0]
    ],
    "med2": [
        [0,0,0, 6,0,0, 4,0,0],
        [7,0,0, 0,0,3, 6,0,0],
        [0,0,0, 0,9,1, 0,8,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,5,0, 1,8,0, 0,0,3],
        [0,0,0, 3,0,6, 0,4,5],
        [0,4,0, 2,0,0, 0,6,0],
        [9,0,3, 0,0,0, 0,0,0],
        [0,2,0, 0,0,0, 1,0,0]
    ],
    "hard1": [
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,3, 0,8,5],
        [0,0,1, 0,2,0, 0,0,0],
        [0,0,0, 5,0,7, 0,0,0],
        [0,0,4, 0,0,0, 1,0,0],
        [0,9,0, 0,0,0, 0,0,0],
        [5,0,0, 0,0,0, 0,7,3],
        [0,0,2, 0,1,0, 0,0,0],
        [0,0,0, 0,4,0, 0,0,9]
    ],
    "hard2": [
        [3,0,6, 5,0,8, 4,0,0],
        [5,2,0, 0,0,0, 0,0,0],
        [0,8,7, 0,0,0, 0,3,1],
        [0,0,3, 0,1,0, 0,8,0],
        [9,0,0, 8,6,3, 0,0,5],
        [0,5,0, 0,9,0, 6,0,0],
        [1,3,0, 0,0,0, 2,5,0],
        [0,0,0, 0,0,0, 0,7,4],
        [0,0,5, 2,0,6, 3,0,0]
    ]
}

def build_sudoku_csp(grid):
    """Return a CSP instance for the given 9x9 grid."""
    vars = [(r, c) for r in range(9) for c in range(9)]
    domains = {}
    for r, c in vars:
        if grid[r][c] == 0:
            domains[(r, c)] = list(range(1, 10))
        else:
            domains[(r, c)] = [grid[r][c]]

    # Precompute neighbors (row, column, block)
    neighbors = {v: set() for v in vars}
    for r, c in vars:
        # same row
        for c2 in range(9):
            if c2 != c:
                neighbors[(r, c)].add((r, c2))
        # same column
        for r2 in range(9):
            if r2 != r:
                neighbors[(r, c)].add((r2, c))
        # same 3x3 block
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if (i, j) != (r, c):
                    neighbors[(r, c)].add((i, j))

    # Convert sets to lists for consistency
    neighbors = {v: list(neighbors[v]) for v in vars}

    def constraint(a, aval, b, bval):
        return aval != bval

    return CSP(vars, domains, neighbors, constraint)

def validate_sudoku(solution):
    """Check that a solved Sudoku assignment is valid."""
    grid = [[solution[(r, c)] for c in range(9)] for r in range(9)]
    def all_unique(nums):
        return sorted(nums) == list(range(1, 10))
    for i in range(9):
        if not all_unique(grid[i]):          # row
            return False
        if not all_unique([grid[r][i] for r in range(9)]):   # column
            return False
    for br in range(3):
        for bc in range(3):
            block = []
            for r in range(br*3, br*3+3):
                for c in range(bc*3, bc*3+3):
                    block.append(grid[r][c])
            if not all_unique(block):
                return False
    return True