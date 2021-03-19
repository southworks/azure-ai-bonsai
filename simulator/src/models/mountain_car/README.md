# Mountain Car for Project Bonsai

## Objective

An underpowered car must climb a one-dimensional hill to reach a target. Unlike MountainCar v0, the action (engine force applied) is allowed to be a continuous value.

The target is on top of a hill on the right-hand side of the car. If the car reaches it or goes beyond, the episode terminates.

On the left-hand side, there is another hill. Climbing this hill can be used to gain potential energy and accelerate towards the target. On top of this second hill, the car cannot go further than a position equal to -1, as if there was a wall. Hitting this limit does not generate a penalty (it might in a more challenging version).

## States

| State                    | Range         |
| ------------------------ | ------------- |
| cart position            | [-1.2..0.6]   |
| cart velocity            | [-0.7..0.7]   |


## Actions

| Action          | Continuous Value                                                         |
| --------------- | -------------------------------------------------------------------------|
| Push Cart Left  | Push car to the left (negative value) or to the right (positive value)   |

## Configuration Parameters

- velocity
- position
