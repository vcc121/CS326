#!/usr/bin/env python
"""
Test suite for Project 4.

Run with: python tests.py
"""

import unittest
import sys
from game import TicTacToe
from minimax import get_best_move as minimax_move
from alphabeta import get_best_move as alphabeta_move
from world import WumpusWorld
from agent import WumpusAgent
from test_layouts import LAYOUTS


# ============================================================================


class TestWumpusPerceptRules(unittest.TestCase):
    """Check that percept generation is correct."""
    
    def test_no_breeze_no_stench(self):
        grid = [
            ["S", "S", "S"],
            ["S", "P", "S"],
            ["S", "W", "S"]
        ]
        world = WumpusWorld(grid)
        percept = world.get_percept((0, 0))
        self.assertFalse(percept["breeze"])
        self.assertFalse(percept["stench"])
    
    def test_breeze_from_pit(self):
        grid = [
            ["S", "P", "S"],
            ["S", "S", "S"],
            ["S", "S", "S"]
        ]
        world = WumpusWorld(grid)
        percept = world.get_percept((0, 0))
        self.assertTrue(percept["breeze"])
        self.assertFalse(percept["stench"])
    
    def test_stench_from_wumpus(self):
        grid = [
            ["S", "W", "S"],
            ["S", "S", "S"],
            ["S", "S", "S"]
        ]
        world = WumpusWorld(grid)
        percept = world.get_percept((0, 0))
        self.assertFalse(percept["breeze"])
        self.assertTrue(percept["stench"])


class TestWumpusKBUpdates(unittest.TestCase):
    """Check that the knowledge base updates after each percept."""
    
    def test_kb_marks_safe_on_no_breeze_no_stench(self):
        world = WumpusWorld(LAYOUTS["4x4_easy"])
        agent = WumpusAgent(world)
        agent.perceive_and_update()
        self.assertTrue(agent.kb.is_safe((1, 0)))
        self.assertTrue(agent.kb.is_safe((0, 1)))
    
    def test_kb_marks_unsafe_from_intersection(self):
        """Two breezy cells sharing exactly one common neighbor → that neighbor is a pit."""
        grid = [
            ["S", "S", "S"],
            ["S", "P", "S"],
            ["S", "S", "S"]
        ]
        world = WumpusWorld(grid)
        agent = WumpusAgent(world)
        # Start at (0,0) – no percepts
        agent.pos = (0, 0)
        agent.perceive_and_update()
        # Move to (1,0) – breeze
        agent.kb.add_visited((1, 0))
        agent.pos = (1, 0)
        agent.perceive_and_update()
        # Move to (0,1) – breeze
        agent.kb.add_visited((0, 1))
        agent.pos = (0, 1)
        agent.perceive_and_update()
        # After both, the common candidate (1,1) should be marked unsafe
        self.assertTrue(agent.kb.is_unsafe((1, 1)))


class TestWumpusNoUnsafeMove(unittest.TestCase):
    """Check that the agent never moves into a square known to be unsafe."""
    
    def test_agent_avoids_unsafe(self):
        grid = [
            ["S", "P", "S"],
            ["S", "S", "S"],
            ["S", "S", "S"]
        ]
        world = WumpusWorld(grid)
        agent = WumpusAgent(world)
        agent.perceive_and_update()
        move = agent.choose_move()
        # Agent should not move into the pit (0,1)
        self.assertNotEqual(move, (0, 1))


# ============================================================================
# Tic-Tac-Toe Tests
# ============================================================================

class TestTicTacToeLegalMoves(unittest.TestCase):
    def test_empty_board_has_nine_moves(self):
        game = TicTacToe()
        self.assertEqual(len(game.get_actions()), 9)
    
    def test_occupied_cells_not_in_actions(self):
        game = TicTacToe()
        game.apply_move((0, 0))
        actions = game.get_actions()
        self.assertNotIn((0, 0), actions)
        self.assertEqual(len(actions), 8)


class TestTicTacToeTerminalStates(unittest.TestCase):
    def test_win_detection_row(self):
        game = TicTacToe()
        game.board = [["X", "X", "X"], [" ", " ", " "], [" ", " ", " "]]
        self.assertTrue(game.is_terminal())
        self.assertEqual(game.utility(), 1)
    
    def test_win_detection_column(self):
        game = TicTacToe()
        game.board = [["X", " ", " "], ["X", " ", " "], ["X", " ", " "]]
        self.assertTrue(game.is_terminal())
        self.assertEqual(game.utility(), 1)
    
    def test_draw_detection(self):
        game = TicTacToe()
        game.board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        self.assertTrue(game.is_terminal())
        self.assertEqual(game.utility(), 0)
    
    def test_non_terminal_board(self):
        game = TicTacToe()
        game.board = [["X", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.assertFalse(game.is_terminal())


class TestMinimaxMoveSelection(unittest.TestCase):
    def test_minimax_wins_immediately(self):
        game = TicTacToe()
        game.board = [["X", "X", " "], ["O", "O", " "], [" ", " ", " "]]
        game.current_player = "X"
        move, _ = minimax_move(game)
        self.assertEqual(move, (0, 2))
    
    def test_minimax_blocks_opponent_win(self):
        game = TicTacToe()
        game.board = [["O", "O", " "], ["X", " ", " "], [" ", " ", " "]]
        game.current_player = "X"
        move, _ = minimax_move(game)
        self.assertEqual(move, (0, 2))
    
    def test_minimax_prefers_win_over_block(self):
        game = TicTacToe()
        game.board = [["X", "X", " "], [" ", " ", " "], ["O", "O", " "]]
        game.current_player = "X"
        move, _ = minimax_move(game)
        self.assertEqual(move, (0, 2))


class TestAlphaBetaConsistency(unittest.TestCase):
    def test_alphabeta_matches_minimax(self):
        game = TicTacToe()
        game.board = [["X", " ", " "], [" ", "O", " "], [" ", " ", " "]]
        game.current_player = "X"
        move_mm, nodes_mm = minimax_move(game)
        move_ab, nodes_ab = alphabeta_move(game)
        self.assertEqual(move_mm, move_ab)
        self.assertLessEqual(nodes_ab, nodes_mm)
    
    def test_alphabeta_never_worse(self):
        game = TicTacToe()
        move_mm, _ = minimax_move(game)
        move_ab, _ = alphabeta_move(game)
        self.assertEqual(move_mm, move_ab)


if __name__ == "__main__":
    unittest.main(verbosity=2)