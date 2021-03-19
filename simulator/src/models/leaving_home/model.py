import math
import random
from typing import ForwardRef
import numpy as np
from collections import namedtuple

default_config = { "initial_room": 2 }

class model:
    def __init__(self):
                                #  0    1    2    3    4    5    6    7    8    9   10
        self.home = np.matrix( [[  1,   0,   0,   0,   1,   0,   0,   0,   0,   1,   0,],  #row 1
                                [  0,   0,   1,   1,   0,   1,   1,   1,   0,   0,   1,],  #row 1
                                [  0,   1,   0,   1,   1,   0,   0,   0,   0,   0,   0,],  #row 2
                                [  0,   1,   1,   0,   0,   0,   0,   0,   0,   1,   1,],  #row 3
                                [  1,   0,   1,   0,   0,   1,   0,   0,   0,   0,   0,],  #row 4
                                [  0,   1,   0,   0,   1,   0,   1,   0,   0,   0,   0,],  #row 5
                                [  0,   1,   0,   0,   0,   1,   0,   1,   0,   0,   0,],  #row 6
                                [  0,   1,   0,   0,   0,   0,   1,   0,   1,   0,   1,],  #row 7
                                [  0,   0,   0,   0,   0,   0,   0,   1,   0,   1,   1,],  #row 8
                                [  1,   0,   0,   1,   0,   0,   0,   0,   1,   0,   1,],  #row 9
                                [  0,   1,   0,   1,   0,   0,   0,   1,   1,   1,   0,]]) #row 10

        self.reset()

    def reset(self, config=default_config):
        """ Reset the model of a leaving home
        """

        self.room = int(config["initial_room"]) if "initial_room" in config.keys() else 2
        self.wrong_room = False
        self.path = []

    def step(self, action):
        """ Move the state to new position depending of the action
        """
        new_room = int(action["new_room"])
        self.wrong_room = False

        available_rooms = self.available_actions(self.room)
        if (new_room not in available_rooms):
            self.wrong_room = True
        else:
            self.path.append(self.room)
            self.room = new_room

        print(str(self.path) + " action: " + str(action))

    def get_state(self):
        return {
            "room": self.room,
            "wrong_room": int(self.wrong_room),
            "available_rooms": {
                "room0": int(self.home[self.room,0]),
                "room1": int(self.home[self.room,1]),
                "room2": int(self.home[self.room,2]),
                "room3": int(self.home[self.room,3]),
                "room4": int(self.home[self.room,4]),
                "room5": int(self.home[self.room,5]),
                "room6": int(self.home[self.room,6]),
                "room7": int(self.home[self.room,7]),
                "room8": int(self.home[self.room,8]),
                "room9": int(self.home[self.room,9]),
                "room10": int(self.home[self.room,10])
            }
        }

    def terminal(self):
        return self.wrong_room or self.room == 0

    def render(self):
        pass

    def available_actions(self, state):
        current_state_row = self.home[state,]
        return np.where(current_state_row > 0)[1]
