import json
import sudoku
import map_coloring

def run_experiments():
    results = []

    # Map coloring
    map_csp = map_coloring.build_map_csp()
    for config in ["baseline", "mrv", "mrv_fc"]:
        sol, metrics = map_csp.solve(config)
        entry = {
            "problem": "map",
            "instance": "Australia",
            "config": config,
            **metrics
        }
        if metrics["solved"]:
            entry["valid"] = map_coloring.validate_map(metrics["solution"])
        results.append(entry)

    # Sudoku
    for name, grid in sudoku.instances.items():
        sudoku_csp = sudoku.build_sudoku_csp(grid)
        for config in ["baseline", "mrv", "mrv_fc"]:
            sol, metrics = sudoku_csp.solve(config)
            entry = {
                "problem": "sudoku",
                "instance": name,
                "config": config,
                **metrics
            }
            if metrics["solved"]:
                entry["valid"] = sudoku.validate_sudoku(metrics["solution"])
            results.append(entry)

    # Output
    print(json.dumps(results, indent=2))
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_experiments()