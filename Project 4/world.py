class WumpusWorld:
    def __init__(self, grid, start=(0, 0)):
        self.grid = grid
        self.size = len(grid)
        self.agent_pos = start
        self.wumpus_found = False
        self.pits = self._find_pits()

    def _find_pits(self):
        pits = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == "P":
                    pits.add((i, j))
        return pits

    def get_percept(self, pos):
        i, j = pos

        breeze = False
        stench = False

        for ni, nj in self._neighbors(i, j):
            if (ni, nj) in self.pits:
                breeze = True
            if self.grid[ni][nj] == "W":
                stench = True

        return {
            "breeze": breeze,
            "stench": stench
        }

    def _neighbors(self, i, j):
        moves = [(1,0), (-1,0), (0,1), (0,-1)]
        result = []

        for di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                result.append((ni, nj))

        return result