# 4x4 Layouts
LAYOUT_4X4_EASY = [
    ["S", "S", "S", "S"],
    ["S", "S", "S", "S"],
    ["S", "S", "S", "P"],
    ["S", "W", "S", "S"]
]

# Modified: start (0,0) safe, pit moved away from start
LAYOUT_4X4_MEDIUM = [
    ["S", "S", "S", "S"],   # row0: start safe
    ["S", "P", "S", "S"],   # pit at (1,1) not adjacent to start
    ["S", "S", "S", "S"],
    ["P", "W", "S", "S"]    # pit and Wumpus far away
]

LAYOUT_4X4_HARD = [
    ["S", "P", "S", "P"],
    ["S", "S", "P", "S"],
    ["P", "S", "W", "S"],
    ["S", "P", "S", "S"]
]

# 5x5 Layouts
LAYOUT_5X5_EASY = [
    ["S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S"],
    ["S", "S", "S", "W", "S"],
    ["S", "S", "P", "S", "S"]
]

# Modified: start (0,0) safe
LAYOUT_5X5_MEDIUM = [
    ["S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "P"],
    ["S", "P", "S", "S", "S"],
    ["P", "S", "W", "S", "S"],
    ["S", "S", "P", "S", "S"]
]

LAYOUT_5X5_HARD = [
    ["S", "P", "S", "P", "S"],
    ["P", "S", "P", "S", "P"],
    ["S", "P", "W", "P", "S"],
    ["P", "S", "P", "S", "P"],
    ["S", "P", "S", "P", "S"]
]

# 7x7 Layouts
LAYOUT_7X7_EASY = [
    ["S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "P", "S", "S", "S", "S"],
    ["S", "S", "S", "W", "S", "S", "S"],
    ["S", "S", "S", "S", "P", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S"]
]

# Modified: start (0,0) safe
LAYOUT_7X7_MEDIUM = [
    ["S", "S", "S", "S", "S", "S", "S"],
    ["S", "P", "S", "S", "P", "S", "S"],
    ["S", "S", "S", "W", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "P", "S"],
    ["S", "S", "P", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S"]
]

LAYOUT_7X7_HARD = [
    ["S", "P", "S", "S", "S", "S", "S"],
    ["S", "S", "W", "S", "S", "S", "S"],
    ["S", "S", "S", "P", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "P", "S"],
    ["S", "S", "P", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S"]
]

# 8x8 Layouts
LAYOUT_8X8_EASY = [
    ["S", "S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "P", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "W", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "P", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S", "S"]
]

# Modified: start (0,0) safe
LAYOUT_8X8_MEDIUM = [
    ["S", "S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "P", "S", "P", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "P", "S"],
    ["S", "S", "S", "W", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "P", "S", "S"],
    ["S", "S", "P", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "S", "S"]
]

LAYOUT_8X8_HARD = [
    ["S", "P", "S", "S", "S", "P", "S", "S"],
    ["S", "S", "W", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "P", "S", "S", "P", "S"],
    ["P", "S", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "P", "S", "W", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "P", "S", "S"],
    ["S", "P", "S", "S", "S", "S", "S", "S"],
    ["S", "S", "S", "S", "S", "S", "P", "S"]
]

# Combine all layouts
LAYOUTS = {
    # 4x4 layouts
    "4x4_easy": LAYOUT_4X4_EASY,
    "4x4_medium": LAYOUT_4X4_MEDIUM,
    "4x4_hard": LAYOUT_4X4_HARD,
    
    # 5x5 layouts
    "5x5_easy": LAYOUT_5X5_EASY,
    "5x5_medium": LAYOUT_5X5_MEDIUM,
    "5x5_hard": LAYOUT_5X5_HARD,
    
    # 7x7 layouts
    "7x7_easy": LAYOUT_7X7_EASY,
    "7x7_medium": LAYOUT_7X7_MEDIUM,
    "7x7_hard": LAYOUT_7X7_HARD,
    
    # 8x8 layouts
    "8x8_easy": LAYOUT_8X8_EASY,
    "8x8_medium": LAYOUT_8X8_MEDIUM,
    "8x8_hard": LAYOUT_8X8_HARD,
}