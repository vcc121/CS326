#!/usr/bin/env python
"""
Run Tic-Tac-Toe experiments:
- 10 games vs random opponent (Minimax)
- 5 games vs scripted opponent (Minimax)
- Same for Alpha-Beta (optional but recommended)
Saves JSON results.
"""

import time
import json
import random
from game import TicTacToe
from agent import TicTacToeAgent
from opponents import RandomOpponent

class ScriptedOpponent:
    """Deterministic opponent: prefers center, then corners, then edges."""
    def choose_move(self, state):
        board = state.board
        # Prefer center
        if board[1][1] == ' ':
            return (1, 1)
        # Then corners
        corners = [(0,0), (0,2), (2,0), (2,2)]
        for c in corners:
            if board[c[0]][c[1]] == ' ':
                return c
        # Then edges
        edges = [(0,1), (1,0), (1,2), (2,1)]
        for e in edges:
            if board[e[0]][e[1]] == ' ':
                return e
        # Fallback (should not happen)
        return state.get_actions()[0]

def run_game(agent_config, opponent, game_id, game_type):
    """Run a single Tic-Tac-Toe game and return result dict."""
    game = TicTacToe()
    agent = TicTacToeAgent(config=agent_config)
    
    moves = []
    total_nodes = 0
    start_time = time.time()
    
    while not game.is_terminal():
        if game.current_player == 'X':
            move, nodes = agent.choose_move(game)
            total_nodes += nodes
            moves.append({"player": "X", "move": move, "nodes": nodes})
        else:
            move = opponent.choose_move(game)
            moves.append({"player": "O", "move": move, "nodes": None})
        game.apply_move(move)
    
    runtime_ms = int((time.time() - start_time) * 1000)
    utility = game.utility()
    if utility == 1:
        result = "win"
    elif utility == -1:
        result = "loss"
    else:
        result = "draw"
    
    return {
        "problem": "tictactoe",
        "config": agent_config,
        "opponent": game_type,
        "game_id": game_id,
        "result": result,
        "runtime_ms": runtime_ms,
        "nodes_evaluated": total_nodes,
        "moves_taken": len([m for m in moves if m["player"] == "X"]),
        "trace": moves,
        "final_board": game.board
    }

def run_experiments():
    """Run all required experiments."""
    random.seed(42)  # for reproducibility
    results = []
    
    # --- Minimax vs Random (10 games) ---
    print("\n=== Minimax vs Random Opponent (10 games) ===")
    for i in range(1, 11):
        print(f"Game {i}...")
        result = run_game("minimax", RandomOpponent(), i, "random")
        results.append(result)
        print(f"  Result: {result['result']}, Nodes: {result['nodes_evaluated']}, Moves: {result['moves_taken']}")
    
    # --- Minimax vs Scripted (5 games) ---
    print("\n=== Minimax vs Scripted Opponent (5 games) ===")
    for i in range(1, 6):
        print(f"Game {i}...")
        result = run_game("minimax", ScriptedOpponent(), i, "scripted")
        results.append(result)
        print(f"  Result: {result['result']}, Nodes: {result['nodes_evaluated']}, Moves: {result['moves_taken']}")
    
    # --- (Optional) Alpha-Beta vs Random (10 games) ---
    print("\n=== Alpha-Beta vs Random Opponent (10 games) ===")
    for i in range(1, 11):
        print(f"Game {i}...")
        result = run_game("alphabeta", RandomOpponent(), i, "random")
        results.append(result)
        print(f"  Result: {result['result']}, Nodes: {result['nodes_evaluated']}, Moves: {result['moves_taken']}")
    
    # --- Alpha-Beta vs Scripted (5 games) ---
    print("\n=== Alpha-Beta vs Scripted Opponent (5 games) ===")
    for i in range(1, 6):
        print(f"Game {i}...")
        result = run_game("alphabeta", ScriptedOpponent(), i, "scripted")
        results.append(result)
        print(f"  Result: {result['result']}, Nodes: {result['nodes_evaluated']}, Moves: {result['moves_taken']}")
    
    # Save all results to a single JSON file
    with open("tictactoe_experiments.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for cfg in ["minimax", "alphabeta"]:
        for opp in ["random", "scripted"]:
            games = [r for r in results if r["config"] == cfg and r["opponent"] == opp]
            wins = sum(1 for g in games if g["result"] == "win")
            draws = sum(1 for g in games if g["result"] == "draw")
            losses = sum(1 for g in games if g["result"] == "loss")
            avg_nodes = sum(g["nodes_evaluated"] for g in games) / len(games) if games else 0
            avg_runtime = sum(g["runtime_ms"] for g in games) / len(games) if games else 0
            print(f"{cfg:10} vs {opp:8} | Wins:{wins:2} Draws:{draws:2} Losses:{losses:2} | Avg nodes:{avg_nodes:8.0f} | Avg runtime:{avg_runtime:6.1f} ms")

if __name__ == "__main__":
    run_experiments()