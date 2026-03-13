import time
from collections import deque


class CSP:
    """
    Generic CSP: variables, domains, neighbors (constraint graph), and binary constraint function.
    Domains are dict var->list(values). Neighbors is dict var->list of other vars with constraints.
    """

    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = variables
        self.original_domains = {v: list(domains[v])[:] for v in variables}
        self.domains = {v: list(domains[v])[:] for v in variables}
        self.neighbors = neighbors
        self.constraint = constraint

        # Metrics
        self.assignments = 0
        self.backtracks = 0

    def reset_domains(self):
        """Reset domains before each solve."""
        self.domains = {v: list(self.original_domains[v])[:] for v in self.variables}

    def is_consistent(self, var, value, assignment):
        """Check consistency of assigning var=value with existing assignment."""
        for other in self.neighbors[var]:
            if other in assignment and not self.constraint(var, value, other, assignment[other]):
                return False
        return True

    def select_unassigned(self, assignment, use_mrv=False, use_degree=False):
        """Select an unassigned variable."""
        unassigned = [v for v in self.variables if v not in assignment]

        if not use_mrv:
            return unassigned[0] if unassigned else None

        best = None
        min_domain = float('inf')

        for v in unassigned:
            dsize = len(self.domains[v])
            if dsize < min_domain:
                best = v
                min_domain = dsize
            elif use_degree and dsize == min_domain:
                if len(self.neighbors[v]) > len(self.neighbors[best]):
                    best = v

        return best

    def order_values(self, var, assignment, use_lcv=False):
        """Return ordered domain values."""
        if not use_lcv:
            return list(self.domains[var])

        def conflict_count(value):
            count = 0
            for nbr in self.neighbors[var]:
                if nbr not in assignment:
                    for val2 in self.domains[nbr]:
                        if not self.constraint(var, value, nbr, val2):
                            count += 1
            return count

        return sorted(self.domains[var], key=conflict_count)

    def forward_check(self, var, value, assignment):
        """Forward checking."""
        removed = []

        for nbr in self.neighbors[var]:
            if nbr not in assignment:
                to_remove = [v for v in self.domains[nbr]
                             if not self.constraint(var, value, nbr, v)]

                if to_remove:
                    for v in to_remove:
                        self.domains[nbr].remove(v)

                    removed.append((nbr, to_remove))

                    if not self.domains[nbr]:
                        return False, removed

        return True, removed

    def restore(self, removed):
        """Restore domains."""
        for var, values in removed:
            self.domains[var].extend(values)

    # -------------------------
    # AC-3 ARC CONSISTENCY
    # -------------------------

    def revise(self, xi, xj):
        """Revise domains for AC3."""
        revised = False
        to_remove = []

        for x in self.domains[xi]:
            if not any(self.constraint(xi, x, xj, y) for y in self.domains[xj]):
                to_remove.append(x)

        if to_remove:
            for v in to_remove:
                self.domains[xi].remove(v)
            revised = True

        return revised

    def ac3(self):
        """AC-3 algorithm."""
        queue = deque([(xi, xj) for xi in self.variables for xj in self.neighbors[xi]])

        while queue:
            xi, xj = queue.popleft()

            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False

                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))

        return True

    # -------------------------

    def backtrack(self, assignment, use_mrv=False, use_fc=False, use_degree=False, use_lcv=False):
        """Backtracking search."""

        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned(assignment, use_mrv, use_degree)

        for value in self.order_values(var, assignment, use_lcv):
            self.assignments += 1

            if self.is_consistent(var, value, assignment):

                assignment[var] = value

                success = True
                removed = []

                if use_fc:
                    success, removed = self.forward_check(var, value, assignment)

                if success:
                    result = self.backtrack(assignment, use_mrv, use_fc, use_degree, use_lcv)

                    if result:
                        return result

                if use_fc:
                    self.restore(removed)

                del assignment[var]

        self.backtracks += 1
        return None

    def solve(self, config):
        """
        config options:
        baseline
        mrv
        mrv_fc
        mrv_fc_ac
        """

        self.reset_domains()

        use_mrv = "mrv" in config
        use_fc = "fc" in config
        use_ac = "ac" in config
        use_degree = use_mrv
        use_lcv = "lcv" in config

        self.assignments = 0
        self.backtracks = 0

        start = time.perf_counter()

        if use_ac:
            if not self.ac3():
                return None, {
                    "solved": False,
                    "runtime_ms": 0,
                    "assignments": 0,
                    "backtracks": 0,
                    "solution": {}
                }

        assignment = {}
        sol = self.backtrack(assignment, use_mrv, use_fc, use_degree, use_lcv)

        end = time.perf_counter()

        runtime_ms = (end - start) * 1000

        return sol, {
            "solved": sol is not None,
            "runtime_ms": runtime_ms,
            "assignments": self.assignments,
            "backtracks": self.backtracks,
            "solution": sol or {}
        }