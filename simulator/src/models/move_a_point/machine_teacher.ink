# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
inkling "2.0"
using Math
using Number
using Goal

const Precision = 0.15
const MaxSteps = 120

type GameState{
    # X and Y direction of the point. These names (and types) have to match the
    # dictionary returned by get_state() our simulator.
    #dx: Number.Float32,
    #dy: Number.Float32
    previous_x: Number.Float32,
    previous_y: Number.Float32,
    source_x: Number.Float32,
    source_y: Number.Float32,
    target_x: Number.Float32,
    target_y: Number.Float32,
}

#type PlayerMove{
type Action {
    # This name (and type) has to match the parameter to advance() in our
    # simulator. We specify the range and step size for the action.
    #Float32{0:1.575:6.283} direction_radians
    direction_radians: Number.Float32<0,1.575,6.283>
    #move: Number.Int8<1, 2, 3, 4, 5, 6, 7, 8, 9>
}

type SimConfig{
    # The sim doesn't have any configuration, but Inkling requires
    # that we have a schema anyway.
    #Int8 dummy
    dummy: Number.Int8
}

function distance(x1: Number.Float32, x2: Number.Float32, y1: Number.Float32, y2: Number.Float32) : Number.Float32{
    #return Math.Sqrt(obs.dx**2-obs.dy**2)
    return Math.Sqrt((x1 - x2)**2 + (y1 - y2) ** 2)
}

function Reward(obs: GameState) {
    var progress : Number.Float32 = 0.0
    # Large penalty for exceeding the buffer queue's capacity.
    # Otherwise, try to maximize the cost per product value.

    progress = distance(obs.previous_x, obs.previous_y, obs.target_x, obs.target_y) - distance(obs.source_x, obs.source_y, obs.target_x, obs.target_y) / 0.1

    if progress > 0 {
    # 0 is a special value
        progress = progress**2
    } else {
        progress = progress * 2
        progress = progress - 1
    }

    return progress
}

# This is the Inkling name of our simulator. It has to match the parameter
# to bonsai.run_for_training_or_prediction(), but does not have to match the
# name of the Python file.
simulator move_a_point_sim(action: Action, config: SimConfig): GameState{
}

function Terminal(obs:GameState)
{
    #Simulation ends if the agent gets close enough to the target position.
    if(distance(obs.source_x, obs.source_y, obs.target_x, obs.target_y) < Precision)
    {
        return true
    }

    # The brain gets one chance at the answer
    return false
}

graph (input: GameState): Action {
    concept find_the_target(input): Action {
        curriculum {
            #simulator play_move_a_point_sim

            source move_a_point_sim
            terminal Terminal
            reward Reward

            training {
                # Limit the number of iterations per episode to 120. The default
                # is 1000, which makes it much tougher to succeed.
                EpisodeIterationLimit: MaxSteps
            }
            #We can define a goal without reward, this goal could be to keep a distance in a range
            #goal (State: GameState) {
            #    maximize `Near to target`: distance(State) in Goal.Range(distance(State)<Precision, distance(State)>Precision)
            #}

            lesson `get_close` {
                # Specify the configuration parameters that should be varied
                # from one episode to the next during this lesson.
                scenario {
                    dummy: Number.Int8<-1>
                    #maximize reward_shaped
                }
            }
        }
    }
    #output find_the_target
}
