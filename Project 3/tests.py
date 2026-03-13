import sudoku
import map_coloring
from csp_solver import CSP

def test_sudoku_validator():
    # A known solved easy1 (you can hardcode a solution or just test a valid grid)
    solved_easy1 = {
        (0,0):5, (0,1):3, (0,2):4, (0,3):6, (0,4):7, (0,5):8, (0,6):9, (0,7):1, (0,8):2,
        (1,0):6, (1,1):7, (1,2):2, (1,3):1, (1,4):9, (1,5):5, (1,6):3, (1,7):4, (1,8):8,
        (2,0):1, (2,1):9, (2,2):8, (2,3):3, (2,4):4, (2,5):2, (2,6):5, (2,7):6, (2,8):7,
        (3,0):8, (3,1):5, (3,2):9, (3,3):7, (3,4):6, (3,5):1, (3,6):4, (3,7):2, (3,8):3,
        (4,0):4, (4,1):2, (4,2):6, (4,3):8, (4,4):5, (4,5):3, (4,6):7, (4,7):9, (4,8):1,
        (5,0):7, (5,1):1, (5,2):3, (5,3):9, (5,4):2, (5,5):4, (5,6):8, (5,7):5, (5,8):6,
        (6,0):9, (6,1):6, (6,2):1, (6,3):5, (6,4):3, (6,5):7, (6,6):2, (6,7):8, (6,8):4,
        (7,0):2, (7,1):8, (7,2):7, (7,3):4, (7,4):1, (7,5):9, (7,6):6, (7,7):3, (7,8):5,
        (8,0):3, (8,1):4, (8,2):5, (8,3):2, (8,4):8, (8,5):6, (8,6):1, (8,7):7, (8,8):9
    }
    assert sudoku.validate_sudoku(solved_easy1) == True

def test_map_validator():
    valid_solution = {
        "WA": "red", "NT": "green", "SA": "blue",
        "Q": "red", "NSW": "green", "V": "red", "T": "red"
    }
    assert map_coloring.validate_map(valid_solution) == True

def test_csp_baseline_sudoku():
    csp = sudoku.build_sudoku_csp(sudoku.instances["easy1"])
    sol, metrics = csp.solve("baseline")
    assert metrics["solved"] == True
    assert sudoku.validate_sudoku(sol) == True

if __name__ == "__main__":
    test_sudoku_validator()
    test_map_validator()
    test_csp_baseline_sudoku()
    print("All tests passed.")