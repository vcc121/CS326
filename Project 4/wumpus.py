from agent import WumpusAgent
from world import WumpusWorld
from test_layouts import LAYOUT_1


def run():
    world = WumpusWorld(LAYOUT_1)
    agent = WumpusAgent(world)

    steps = 10

    for _ in range(steps):
        print("Agent at:", agent.pos)

        agent.perceive_and_update()

        move = agent.choose_move()

        print("Moving to:", move)

        agent.pos = move

        if move in world.pits:
            print("💀 Fell into a pit!")
            break

        if world.grid[move[0]][move[1]] == "W":
            print("👹 Found Wumpus!")
            break


if __name__ == "__main__":
    run()