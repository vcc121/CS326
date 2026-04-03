class KnowledgeBase:
    def __init__(self):
        self.safe = set()
        self.unsafe = set()
        self.visited = set()
        self.unknown = set()

    def mark_safe(self, cell):
        self.safe.add(cell)
        self.unsafe.discard(cell)

    def mark_unsafe(self, cell):
        if cell not in self.safe:
            self.unsafe.add(cell)

    def is_safe(self, cell):
        return cell in self.safe

    def is_unsafe(self, cell):
        return cell in self.unsafe

    def add_visited(self, cell):
        self.visited.add(cell)
        self.safe.add(cell)