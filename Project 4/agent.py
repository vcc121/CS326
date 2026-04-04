from collections import deque
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
        self.size = world.size
        self.kb.add_visited(self.pos)

        # Pit inference structures
        self.pit_candidates = {}   # breezy cell -> set of possible pit neighbors

    def get_neighbors(self, pos):
        return self.world._neighbors(*pos)

    def perceive_and_update(self):
        percept = self.world.get_percept(self.pos)
        neighbors = self.get_neighbors(self.pos)

        # --- Pit inference from no breeze ---
        if not percept["breeze"]:
            for n in neighbors:
                self.kb.mark_pit_free(n)
        else:
            # This cell has a breeze: record possible pit candidates
            possible = {n for n in neighbors if n not in self.kb.pit_free}
            if possible:
                if self.pos in self.pit_candidates:
                    self.pit_candidates[self.pos] &= possible
                else:
                    self.pit_candidates[self.pos] = possible

        # --- CRITICAL FIX: Deduce pits from multiple breezy cells ---
        # After updating candidates, check for intersections across different breezy cells
        changed = True
        while changed:
            changed = False
            
            # Method 1: If any candidate set has size 1, that's a pit
            for breezy, pits in list(self.pit_candidates.items()):
                if len(pits) == 1:
                    pit = next(iter(pits))
                    if pit not in self.kb.unsafe:
                        self.kb.mark_unsafe(pit)
                        changed = True
                        
                        # Remove this pit from ALL candidate sets
                        for b in list(self.pit_candidates.keys()):
                            if pit in self.pit_candidates[b]:
                                self.pit_candidates[b].discard(pit)
            
            # Method 2: If two different breezy cells share exactly one common candidate, that's a pit
            breezy_cells = list(self.pit_candidates.keys())
            for i in range(len(breezy_cells)):
                for j in range(i + 1, len(breezy_cells)):
                    intersection = self.pit_candidates[breezy_cells[i]] & self.pit_candidates[breezy_cells[j]]
                    if len(intersection) == 1:
                        pit = next(iter(intersection))
                        if pit not in self.kb.unsafe:
                            self.kb.mark_unsafe(pit)
                            changed = True
                            # Remove from all candidate sets
                            for b in list(self.pit_candidates.keys()):
                                if pit in self.pit_candidates[b]:
                                    self.pit_candidates[b].discard(pit)

        # --- Wumpus inference (unchanged) ---
        if not percept["stench"]:
            for n in neighbors:
                self.kb.mark_wumpus_free(n)
        else:
            possible_w = {n for n in neighbors if n not in self.kb.wumpus_free}
            if len(possible_w) == 1:
                w = next(iter(possible_w))
                self.kb.known_wumpus = w
                self.kb.mark_unsafe(w)
                self.kb.propagate_wumpus_free(self.size)

        # --- Additional inference (unchanged) ---
        safe_neighbors = [n for n in neighbors if self.kb.is_safe(n)]
        if len(safe_neighbors) == len(neighbors) - 1:
            for n in neighbors:
                if not self.kb.is_safe(n):
                    self.kb.mark_unsafe(n)

        # --- Mark pit-free cells adjacent to breezy cells but not in candidate sets ---
        for breezy, pits in self.pit_candidates.items():
            for n in self.get_neighbors(breezy):
                if n not in pits and n not in self.kb.pit_free and n not in self.kb.unsafe:
                    self.kb.mark_pit_free(n)

    def find_path(self, allow_unknown=False):
        """BFS to nearest unvisited cell. Only moves into safe cells."""
        allowed = set(self.kb.safe)
        allowed.add(self.pos)

        queue = deque([(self.pos, [self.pos])])
        seen = {self.pos}

        while queue:
            current, path = queue.popleft()
            if current in self.kb.frontier_safe():
                return path

            for n in self.get_neighbors(current):
                if n in seen:
                    continue
                if n in self.kb.unsafe:
                    continue
                if not allow_unknown and n not in self.kb.safe:
                    continue
                seen.add(n)
                queue.append((n, path + [n]))
        return None

    def choose_move(self):
        path = self.find_path(allow_unknown=False)
        if path and len(path) > 1:
            next_move = path[1]
            self.kb.add_visited(next_move)
            return next_move

        print("No provably safe moves left. Agent stopping.")
        return self.pos