import time
import json
import sys
from agent import WumpusAgent
from world import WumpusWorld
from test_layouts import LAYOUTS


def run(instance="layout3", config="kb", max_steps=50):
    if instance not in LAYOUTS:
        print(f"Error: Layout '{instance}' not found. Available: {list(LAYOUTS.keys())}")
        return None
    
    grid = LAYOUTS[instance]
    world = WumpusWorld(grid)
    agent = WumpusAgent(world)

    trace = []
    moves = 0
    success = True

    start_time = time.time()

    for step in range(max_steps):
        percept = world.get_percept(agent.pos)

        trace.append({
            "step": step,
            "position": agent.pos,
            "percept": percept
        })

        print(f"Step {step} | Pos: {agent.pos} | Percept: {percept}")

        agent.perceive_and_update()
        move = agent.choose_move()
        if move == agent.pos:
            print("No progress possible. Stopping.")
            break
        
        print(f"Moving to: {move}")

        # Check for hazards BEFORE moving
        if move in world.pits:
            print(f"Fell into a pit at {move}!")
            success = False
            trace.append({
                "step": step + 1,
                "position": move,
                "percept": world.get_percept(move),
                "death": "pit"
            })
            break

        if world.grid[move[0]][move[1]] == "W":
            print(f"Eaten by Wumpus at {move}!")
            success = False
            trace.append({
                "step": step + 1,
                "position": move,
                "percept": world.get_percept(move),
                "death": "wumpus"
            })
            break

        agent.pos = move
        moves += 1

    runtime = int((time.time() - start_time) * 1000)

    result = {
        "problem": "wumpus",
        "instance": instance,
        "config": config,
        "success": success,
        "runtime_ms": runtime,
        "moves_taken": moves,
        "grid_size": len(grid),
        "trace": trace
    }

    print("\n" + "="*50)
    print(f"Final Result:")
    print(f"  Instance: {instance}")
    print(f"  Grid size: {len(grid)}x{len(grid)}")
    print(f"  Success: {success}")
    print(f"  Moves taken: {moves}")
    print(f"  Runtime: {runtime} ms")
    print("="*50)

    # Save JSON
    filename = f"wumpus_{instance}.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=4)
    print(f"\nResults saved to {filename}")

    return result


if __name__ == "__main__":
    # Run multiple layouts for testing
    if len(sys.argv) > 1:
        # Run specific layout from command line
        instance = sys.argv[1]
        run(instance)
    else:
        # Test all layouts
        print("Testing all Wumpus World layouts...\n")
        
        layouts_to_test = [
            "4x4_easy", "4x4_medium", "4x4_hard",
            "5x5_easy", "5x5_medium", "5x5_hard",
            "7x7_easy", "7x7_medium", "7x7_hard",
            "8x8_easy", "8x8_medium", "8x8_hard"
        ]
        
        results_summary = []
        for layout in layouts_to_test:
            print(f"\n{'='*60}")
            print(f"Testing layout: {layout}")
            print(f"{'='*60}")
            result = run(layout, max_steps=100)
            if result:
                results_summary.append({
                    "layout": layout,
                    "success": result["success"],
                    "moves": result["moves_taken"],
                    "runtime": result["runtime_ms"]
                })
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY OF ALL RUNS")
        print("="*60)
        for r in results_summary:
            status = "SUCCESS" if r["success"] else "FAILED"
            print(f"{r['layout']:12} | {status} | Moves: {r['moves']:3} | Runtime: {r['runtime']:3} ms")