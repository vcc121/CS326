class KnowledgeBase:
    def __init__(self):
        self.safe = set()
        self.unsafe = set()
        self.visited = set()
        self.pit_free = set()
        self.wumpus_free = set()
        self.known_wumpus = None

    def mark_safe(self, cell):
        self.safe.add(cell)
        self.unsafe.discard(cell)
        self.pit_free.add(cell)
        self.wumpus_free.add(cell)

    def mark_unsafe(self, cell):
        if cell not in self.safe:
            self.unsafe.add(cell)

    def mark_pit_free(self, cell):
        self.pit_free.add(cell)
        if cell in self.wumpus_free:
            self.mark_safe(cell)

    def mark_wumpus_free(self, cell):
        self.wumpus_free.add(cell)
        if cell in self.pit_free:
            self.mark_safe(cell)

    def add_visited(self, cell):
        self.visited.add(cell)
        self.mark_safe(cell)

    def is_safe(self, cell):
        return cell in self.safe

    def is_unsafe(self, cell):
        return cell in self.unsafe

    def is_unknown(self, cell):
        return cell not in self.safe and cell not in self.unsafe

    def frontier_safe(self):
        return self.safe - self.visited

    def propagate_wumpus_free(self, size):
        if self.known_wumpus is None:
            return
        for i in range(size):
            for j in range(size):
                cell = (i, j)
                if cell != self.known_wumpus:
                    self.mark_wumpus_free(cell)