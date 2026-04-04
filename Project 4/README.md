File Structure
text
project_root/
├── agent.py               # TicTacToeAgent and WumpusAgent classes
├── alphabeta.py           # Alpha‑Beta pruning implementation
├── game.py                # TicTacToe game logic (board, moves, terminal test)
├── kb.py                  # KnowledgeBase for Wumpus (safe/unsafe, pit_free, wumpus_free)
├── minimax.py             # Minimax search implementation
├── opponents.py           # RandomOpponent (and ScriptedOpponent defined in experiments)
├── test_layouts.py        # All Wumpus layouts (4x4, 5x5, 7x7, 8x8, easy/medium/hard)
├── world.py               # WumpusWorld environment (percepts, neighbors, pits)
├── wumpus.py              # Run a single Wumpus layout or all layouts (saves JSON)
├── wumpus_experiments.py  # Run all Wumpus layouts sequentially
├── tictactoe.py           # Run a single Tic‑Tac‑Toe game (Minimax vs Random)
├── tictactoe_experiments.py # Run 30 games (Minimax/Alpha‑Beta vs Random/Scripted)
└── README.md              # This file
Requirements
Python 3.8 or higher.

No external libraries – uses only random, time, json, collections, sys.

Running Instructions
1. Wumpus World
Run a single layout
bash
python wumpus.py <layout_name>
Example:

bash
python wumpus.py 8x8_easy
Available layout names:
4x4_easy, 4x4_medium, 4x4_hard,
5x5_easy, 5x5_medium, 5x5_hard,
7x7_easy, 7x7_medium, 7x7_hard,
8x8_easy, 8x8_medium, 8x8_hard

Run all layouts (default)
bash
python wumpus.py
This runs every layout in test_layouts.py and saves a separate JSON file for each.

Run via the experiment script
bash
python wumpus_experiments.py
Same as python wumpus.py – runs all layouts.

Output
Terminal: step‑by‑step percepts, moves, final summary.

JSON file: wumpus_<layout_name>.json containing problem, instance, config, success, runtime_ms, moves_taken, grid_size, trace.

2. Tic‑Tac‑Toe
Run a single game (Minimax vs Random)
bash
python tictactoe.py
The AI plays as X (Maximizing player).

Opponent is random.

Prints the board after each move, final result, and saves nothing (use experiments for JSON).

Run full experiments (required for Option B)
bash
python tictactoe_experiments.py
This runs:

10 games Minimax vs Random

5 games Minimax vs Scripted

10 games Alpha‑Beta vs Random

5 games Alpha‑Beta vs Scripted

Output:

Terminal: progress per game, final summary table with wins, average nodes, runtime.

JSON file: tictactoe_experiments.json containing an array of all game results, each with:

problem, config, opponent, game_id, result (win/loss/draw)

runtime_ms, nodes_evaluated, moves_taken, trace, final_board

Interpreting Results
Wumpus JSON fields
success – true if agent never entered a pit or the Wumpus.

moves_taken – number of moves performed.

trace – list of steps with position and percept.

If success is false, a death field indicates "pit" or "wumpus".

Tic‑Tac‑Toe JSON fields
result – "win", "loss", or "draw".

nodes_evaluated – total number of game states explored (for the AI’s moves only).

trace – each move with player, move coordinates, and (for AI) nodes evaluated.

Example Commands (Quick Start)
bash
# Wumpus World
python wumpus.py 4x4_easy
python wumpus.py                      # all layouts
python wumpus_experiments.py          # same as above

# Tic‑Tac‑Toe
python tictactoe.py                   # single game vs random
python tictactoe_experiments.py       # full 30‑game experiment suite
Notes
The Wumpus agent never guesses – it only moves into squares proved safe (both pit‑free and wumpus‑free). On layouts where the start cell has a breeze or stench, it may stop immediately. This is correct behaviour.

Alpha‑Beta pruning is implemented as an optimisation – it returns the same move as Minimax but evaluates far fewer nodes.
