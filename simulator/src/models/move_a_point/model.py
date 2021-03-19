"""
A simple simulator for learning to move a 2D point to a target location.
"""
from __future__ import print_function
import math
import sys
from random import random

#import bonsai_ai

default_config = {"dummy": -1}

def debug(*args):
    # To debug, change this to True
    if False:
        print(*args, file=sys.stderr)

def distance(p1, p2):
    """Return the euclidean distance between (x1, y1) and (x2, y2)"""
    x1,y1 = p1
    x2,y2 = p2
    return math.hypot(x1-x2, y1-y2)

class model:
    """
    Simulate an agent moving in the plane that contains a target point.
    The simulation takes moves and computes the states that result from those moves.
    """

    STEP_SIZE = 0.1  # how far to step each turn
    PRECISION = 0.15 # For the simple task, let's just get to the right
                      # area -- no need to make the AI learn to work
                      # around the fixed step size by detouring.

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self, config=default_config):
        """
        Reset simulation state -- call before each episode.
        """
        debug('reset')
        def choose_points():
            # Target is a random point in [0,1]**2
            self.target = (random(), random())
            # same for starting point
            self.current = (random(), random())
            self.previous = self.current

        choose_points()
        # re-choose till we start far enough away
        #while self.game_over():
         #   choose_points()

        self.steps = 0
        self.initial_distance = distance(self.current, self.target)
        self.num_episodes = 1

        print("Reset: current: " + str(self.current) + " Target: " + str(self.target) + "initial distance: " + str(self.initial_distance))

    def step(self, action):
        direction_radians = action["direction_radians"]
        """
        Take a step in the specified direction.
        (Note: function name could be read as bo†h "step the simulation time one tick"
         and "take a step in a direction")

        Args:
            direction_radians: where to go
        """
        debug("step", direction_radians)
        self.previous = self.current
        self._move_current(direction_radians)
        self.steps += 1

        print("Previous: " + str(self.previous))
        print("Current: " + str(self.current))
        print("Distance after step: " + str(distance(self.current, self.target)))

    def get_state(self):
        current = self.current
        target = self.target

        previous = self.previous
        # state = {"dx": target[0] - current[0],
        #          "dy": target[1] - current[1],}

        state = {"previous_x": previous[0], "previous_y": previous[1],"source_x": current[0], "source_y": current[1],
                "target_x": target[0], "target_y": target[1]}

        return state

    def terminal(self):
        return False

    def render(self):
        pass

    def game_over(self):
        """
        Simulation ends if the agent gets close enough to the target
        position.
        """
        return distance(self.current, self.target) < self.PRECISION

    def _move_current(self, direction_radians):
        """
        Move the current point STEP_SIZE in the given direction.
        """
        new_x = self.current[0] + self.STEP_SIZE * math.cos(direction_radians)
        new_y = self.current[1] + self.STEP_SIZE * math.sin(direction_radians)

        print("move_current x: " + str(new_x) + "move_current y: " +str(new_y))

        self.current = (new_x, new_y)
