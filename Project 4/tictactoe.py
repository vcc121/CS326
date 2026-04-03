# tictactoe.py

from game import TicTacToe
from agent import TicTacToeAgent
from opponents import RandomOpponent


def run_game(config="minimax"):
    game = TicTacToe()
    agent = TicTacToeAgent(config=config)
    opponent = RandomOpponent()

    moves = []
    total_nodes = 0

    print("\nStarting Tic-Tac-Toe...\n")

    while not game.is_terminal():
        game.print_board()
        print()

        if game.current_player == 'X':
            move, nodes = agent.choose_move(game)
            total_nodes += nodes
            print(f"AI ({config}) chooses: {move} | Nodes evaluated: {nodes}")
        else:
            move = opponent.choose_move(game)
            print(f"Opponent chooses: {move}")

        game.apply_move(move)
        moves.append(move)

    # Final board
    print("\nFinal Board:")
    game.print_board()

    result = game.utility()

    if result == 1:
        print("\nResult: AI (X) wins")
        result_str = "win"
    elif result == -1:
        print("\nResult: Opponent (O) wins")
        result_str = "loss"
    else:
        print("\nResult: Draw")
        result_str = "draw"

    return {
        "result": result_str,
        "moves": moves,
        "nodes_evaluated": total_nodes
    }



if __name__ == "__main__":
    run_game(config="minimax")