#!/usr/bin/env python
"""
Run Wumpus World experiments on all layouts.
Saves JSON results for each layout.
"""

import sys
import os
from wumpus import run as run_wumpus
from test_layouts import LAYOUTS

def run_all_layouts(max_steps=100):
    """Run Wumpus agent on every layout defined in LAYOUTS."""
    results = []
    for layout_name in LAYOUTS.keys():
        print(f"\n{'='*70}")
        print(f"Running Wumpus layout: {layout_name}")
        print(f"{'='*70}")
        result = run_wumpus(instance=layout_name, config="kb", max_steps=max_steps)
        if result:
            results.append(result)
    return results

if __name__ == "__main__":
    # Optionally accept a specific layout from command line
    if len(sys.argv) > 1:
        run_wumpus(sys.argv[1])
    else:
        run_all_layouts()