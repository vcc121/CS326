import json
import os

import sudoku
import map_coloring


def run_experiments():

    print("\nStarting CSP experiments...\n")

    map_configs = [
        "baseline",
        "mrv",
        "mrv_fc",
        "mrv_fc_ac"
    ]

    sudoku_easy_configs = [
        "mrv",
        "mrv_fc",
        "mrv_fc_ac"
    ]

    sudoku_hard_configs = [
        "mrv_fc",
        "mrv_fc_ac"
    ]

    results = []
    run_count = 1

    # ----------------------------
    # MAP COLORING
    # ----------------------------

    print("Running Map Coloring Experiments\n")

    for config in map_configs:

        print(f"[Run {run_count}] Map | config={config}")

        map_csp = map_coloring.build_map_csp()
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

        run_count += 1

    print("\nMap Coloring Experiments Complete\n")

    # ----------------------------
    # SUDOKU
    # ----------------------------

    print("Running Sudoku Experiments\n")

    for name, grid in sudoku.instances.items():

        # detect difficulty by name
        if name.lower() == "easy1":
            configs = ["baseline", "mrv", "mrv_fc", "mrv_fc_ac"]

        elif "hard" in name.lower():
            configs = ["mrv_fc", "mrv_fc_ac"]
        else:
            configs = sudoku_easy_configs

        for config in configs:

            print(f"[Run {run_count}] Sudoku | puzzle={name} | config={config}")

            sudoku_csp = sudoku.build_sudoku_csp(grid)
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

            run_count += 1

    print("\nSudoku Experiments Complete\n")

    # ----------------------------
    # JSON OUTPUT
    # ----------------------------

    # Convert tuple keys so JSON can store Sudoku solutions
    for r in results:
        if "solution" in r and isinstance(r["solution"], dict):
            r["solution"] = {str(k): v for k, v in r["solution"].items()}

    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_dir, "experiment_results.json")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("Results saved to:", output_path)
    print(f"\nAll experiments finished. Total runs: {len(results)}\n")


if __name__ == "__main__":
    run_experiments()