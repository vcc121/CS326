from csp_solver import CSP

# Australia map
variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
domains = {v: ["red", "green", "blue"] for v in variables}
neighbors = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "SA", "Q"],
    "SA": ["WA", "NT", "Q", "NSW", "V"],
    "Q": ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V": ["SA", "NSW"],
    "T": []
}

def constraint(a, aval, b, bval):
    return aval != bval

def build_map_csp():
    return CSP(variables, domains, neighbors, constraint)

def validate_map(solution):
    """Check that all adjacent regions have different colors."""
    for var, color in solution.items():
        for nbr in neighbors[var]:
            if nbr in solution and solution[nbr] == color:
                return False
    return True