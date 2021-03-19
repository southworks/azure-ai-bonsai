inkling "2.0"
using Number
using Math
using Goal

# constants describing the velocity state
const min_velocity = -0.71
const max_velocity = 0.71

# constants describing the position state
const min_position = -1.21
const max_position = 0.61

# constant describing the action value
#The action will be a continuous value between -1 and 1
const min_action = -1.0
const max_action = 1.0

# constants describing the goal values
const min_goal = 0.3
const max_goal = 0.4

type State {
    velocity: number,
    position: number
}

type Action {
    command: number<min_action..max_action>
}

# Configuration variables for the simulator
# These can be accessed by the event loop in your client code.
# velocity: the velocity of the car
# position: the position of the car
type SimConfig {
    velocity: number,
    position: number
}

graph (input: State): Action {
    concept MountainCar(input): Action {
        curriculum {
            source simulator (Action: Action, Config: SimConfig): State {
            }

            goal (State: State) {
                reach ReachTop:
                    State.position in Goal.Range(min_goal,max_goal)
                avoid OutOfRangeOnTheRight:
                    State.position in Goal.RangeAbove(max_position)
                avoid OutOfRangeOnTheLeft:
                    State.position in Goal.RangeBelow(min_position)
                avoid OutOfMaxVelocity:
                    State.velocity in Goal.RangeAbove(max_velocity)
                avoid OutOfMinVelocity:
                    State.velocity in Goal.RangeBelow(min_velocity)
            }

            lesson `Initial config` {
                scenario {
                    velocity: number<0>,
                    position: number<-0.4>
                }
                training {
                    # This lesson finishes when the brain reaches 100% of the goals
                    LessonSuccessThreshold: 1
                }
            }

            lesson `Vary Initial config` {
                scenario {
                    velocity: number<0>,
                    position: number<-0.4..-0.3 step 0.025>
                }
                training {

                    LessonSuccessThreshold: 1
                }
            }

            training {
                # Iterations per episode 2000
                EpisodeIterationLimit: 2000,
                # Finish the training when the brain doesn't progress for 500000 iterations.
                NoProgressIterationLimit: 500000
            }
        }
    }
}
