How to Run

1. Set parameters in main.py:

m, n = 5, 5            # Grid size
start = (0, 0)          # Start location
goal = (4, 4)           # Goal location
min_cost, max_cost = 1, 5
seed = 42               # Random seed

2. Run main.py


3. Check output:

Results are saved to Project 1\results.json

Example Output
{
    "algorithm": "bfs",
    "path": [[0,0],[0,1],[1,1],[2,1],[3,1],[4,1],[4,2],[4,3],[4,4]],
    "steps": 8,
    "total_cost": 8,
    "expanded": 15,
    "generated": 20,
    "max_frontier": 10,
    "runtime_ms": 0.23,
    "status": "success",
    "m": 5,
    "n": 5,
    "start": [0,0],
    "goal": [4,4],
    "min_cost": 1,
    "max_cost": 5,
    "seed": 42
}

How to Test

1. Run Main

2. Test results print into terminal

Notes:

main.py is easy to adjust. All parameters are at the top.
JSON output is formatted and ready for experiments or plotting.
Seed, grid size, and other parameters can be adjusted by changing their variable in main.
Other parts which may raise questions I have tried to leave comments on, for clarity.