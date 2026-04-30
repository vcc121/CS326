# transposition_table.py
import threading

# Node type flags for correct TT lookups
EXACT = 0        # Value is the true minimax score (PV node)
LOWER_BOUND = 1  # Value is a lower bound; real score may be higher (cut node / fail-high)
UPPER_BOUND = 2  # Value is an upper bound; real score may be lower (all node / fail-low)

class TranspositionTable:
    def __init__(self):
        self.table = {}
        self.lock = threading.RLock()

    def store(self, key, depth, value, move, flag=EXACT):
        """Store a search result with its node type flag."""
        with self.lock:
            # Only overwrite if new entry has greater or equal depth
            if key in self.table and self.table[key][0] > depth:
                return
            self.table[key] = (depth, value, move, flag)

    def lookup(self, key):
        """Retrieve a stored result. Returns (depth, value, move, flag) or None."""
        with self.lock:
            return self.table.get(key, None)