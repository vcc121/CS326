How to Run

Run the experiment script to see all experiments run:

python experiments.py

This will:

Execute all required CSP configurations.

Run the solver on all Sudoku puzzles and the map coloring problem.

Save results to:

experiment_results.json


Run the main script to see each puzzle run once:

python main.py

This will:

Run the solver on each of the Sudoku puzzles and the map coloring problem.

Save results to:

results.json


Optional validation tests can also be run using:

python tests.py

These tests confirm that returned solutions satisfy the Sudoku and map coloring constraints.



Why Some Configurations Are Excluded

Certain configurations are intentionally excluded from specific Sudoku puzzles to prevent extremely long runtimes.

Baseline Backtracking

Baseline search does not use any heuristics or domain pruning.
For larger Sudoku puzzles this can cause the search tree to grow extremely large.

Because of this, baseline is only run on the easy1 Sudoku puzzle.
This still provides a useful comparison point for showing how heuristics improve performance, while avoiding excessive computation on harder puzzles.

MRV Without Forward Checking

MRV improves variable selection but does not eliminate invalid values from neighboring domains. On harder Sudoku puzzles this can still lead to very deep search trees.

For this reason, MRV alone is not used on the hard Sudoku puzzles.
Instead, the solver uses:

mrv_fc

mrv_fc_ac

These configurations include stronger constraint propagation and solve difficult puzzles much more efficiently.
