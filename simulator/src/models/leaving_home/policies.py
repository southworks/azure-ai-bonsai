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
        'new_room': random.randint(0, 10)
    }
    return action

def coast(state):
    """
    Ignore the state, go straight.
    """
    action = {
        'new_room': 1
    }
    return action

POLICIES = {"random": random_policy,
            "coast": coast}