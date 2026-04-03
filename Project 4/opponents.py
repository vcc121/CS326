#opponents.py

import random

class RandomOpponent:

    def choose_move(self, state):
        actions = state.get_actions()
        return random.choice(actions)