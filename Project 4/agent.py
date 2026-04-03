# agent.py

from minimax import get_best_move as minimax_move
from alphabeta import get_best_move as alphabeta_move
from kb import KnowledgeBase


class TicTacToeAgent:
    def __init__(self, config="minimax"):
        self.config = config

    def choose_move(self, state):
        if self.config == "minimax":
            return minimax_move(state)

        elif self.config == "alphabeta":
            return alphabeta_move(state)

        else:
            raise ValueError("Unknown config")

class WumpusAgent:
    def __init__(self, world):
        self.world = world
        self.kb = KnowledgeBase()
        self.pos = (0, 0)
        self.kb.add_visited(self.pos)

    def get_neighbors(self, pos):
        return self.world._neighbors(*pos)

    def perceive_and_update(self):
        percept = self.world.get_percept(self.pos)

        neighbors = self.get_neighbors(self.pos)

        # RULE 1: No breeze → neighbors safe from pits
        if not percept["breeze"]:
            for n in neighbors:
                self.kb.mark_safe(n)

        # RULE 2: No stench → neighbors safe from wumpus
        if not percept["stench"]:
            for n in neighbors:
                self.kb.mark_safe(n)

        # RULE 3: if breeze → neighbors might be unsafe (pit risk)
        if percept["breeze"]:
            for n in neighbors:
                if n not in self.kb.safe:
                    self.kb.mark_unsafe(n)

        # RULE 4: if stench → possible wumpus
        if percept["stench"]:
            for n in neighbors:
                if n not in self.kb.safe:
                    self.kb.mark_unsafe(n)

    def choose_move(self):
        neighbors = self.get_neighbors(self.pos)

        # prefer safe unvisited
        for n in neighbors:
            if self.kb.is_safe(n) and n not in self.kb.visited:
                return n

        # fallback: any safe
        for n in neighbors:
            if self.kb.is_safe(n):
                return n

        # last resort (unknown but not known unsafe)
        for n in neighbors:
            if not self.kb.is_unsafe(n):
                return n

        return self.pos  # stuck