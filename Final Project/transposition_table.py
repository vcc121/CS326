# transposition_table.py
import threading

class TranspositionTable:
    def __init__(self):
        self.table = {}
        self.lock = threading.RLock()

    def store(self, key, depth, value, move):
        """Store a search result for a given position key."""
        with self.lock:
            # Only store if the new depth is greater or equal
            if key in self.table and self.table[key][0] > depth:
                return
            self.table[key] = (depth, value, move)

    def lookup(self, key):
        """Retrieve a stored result for a position key."""
        with self.lock:
            return self.table.get(key, None)
