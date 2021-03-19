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
        'hip_1': random.randint(-1, 1),
        'knee_1': random.randint(-1, 1),
        'hip_2': random.randint(-1, 1),
        'knee_2': random.randint(-1, 1)
    }
    return action

def coast(state):
    """
    Ignore the state, go straight.
    """
    action = {
        'hip_1': 1,
        'knee_1': 1,
        'hip_2': 1,
        'knee_2': 1
    }
    return action

POLICIES = {"random": random_policy,
            "coast": coast}