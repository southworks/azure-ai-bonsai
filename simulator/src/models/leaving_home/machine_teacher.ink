# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
inkling "2.0"
using Number

type Rooms number<0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10>

type State {
    room: Rooms,
    wrong_room: Number.Bool,
    available_rooms: {
        room0: Number.Bool,
        room1: Number.Bool,
        room2: Number.Bool,
        room3: Number.Bool,
        room4: Number.Bool,
        room5: Number.Bool,
        room6: Number.Bool,
        room7: Number.Bool,
        room8: Number.Bool,
        room9: Number.Bool,
        room10: Number.Bool
    }
}

type Action {
    new_room: Rooms
}

simulator bonsai_strategy(action: Action, config: SimConfig): State {
}

type SimConfig{
    initial_room: Number.Int8
}

function Reward(obs: State, act: Action) {
    if(obs.wrong_room) {
        return -50
    } else if(obs.room == 0) {
        return 100
    } else {
        return -10
    }
}

function Terminal(obs: State, act: Action){
    return obs.wrong_room or obs.room == 0
}

graph (input: State): Action {
    concept scape_room(input): Action {
        curriculum {
            source bonsai_strategy

            reward Reward
            terminal Terminal

            lesson `Initial Room Predefined` {
                scenario {
                    initial_room: 1
                }

                training {
                    LessonRewardThreshold: 0
                }
            }

            lesson `Vary Initial Room` {
                scenario {
                    initial_room: Number.Int8<1,2,3,4,5,6,7,8,9,10>
                }
            }

            training {
                EpisodeIterationLimit: 100
            }
        }
    }
}
