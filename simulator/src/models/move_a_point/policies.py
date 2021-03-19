"""
Fixed policies to test our sim integration with. These are intended to take
Brain states and return Brain actions.
"""

import random

def random_policy(state):
    """
    Ignore the state, move randomly.
    """
    action = {
        'direction_radians': random.randint(0, 1)
    }
    return action

def coast(state):
    """
    Ignore the state, go straight.
    """
    action = {
        'direction_radians': 1
    }
    return action

POLICIES = {"random": random_policy,
            "coast": coast}