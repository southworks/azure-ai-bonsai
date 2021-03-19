inkling "2.0"
using Number
using Math

const SCALE  = 30.0   # affects how fast-paced the game is, forces should be adjusted as well
const MOTORS_TORQUE = 80

const TERRAIN_LENGTH = 200     # in steps
const TERRAIN_GRASS    = 10    # low long are grass spots, in steps
const TERRAIN_STEP   = 14/SCALE

# constants describing the goal values
const min_action = -1
const max_action = 1

type State {
    hull_angle: number,
    hull_position_0: number,
    hull_position_1: number,
    hull_angularVelocity: number,
    vel_x: number,
    vel_y: number,
    hip_joint_1_angle: number,
    hip_joint_1_speed: number,
    hip_joint_1_motor_speed: number,
    knee_joint_1_angle: number,
    knee_joint_1_speed: number,
    knee_joint_1_motor_speed: number,
    leg_1_ground_contact_flag: number,
    hip_joint_2_angle: number,
    hip_joint_2_speed: number,
    hip_joint_2_motor_speed: number,
    knee_joint_2_angle: number,
    knee_joint_2_speed: number,
    knee_joint_2_motor_speed: number,
    leg_2_ground_contact_flag: number,
    game_over: number,
    preview_shaping: number,
    lidar_0: number,
    lidar_1: number,
    lidar_2: number,
    lidar_3: number,
    lidar_4: number,
    lidar_5: number,
    lidar_6: number,
    lidar_7: number,
    lidar_8: number,
    lidar_9: number
}

# Even though the ObservableState removes the preview_shaping variable, this could
# be calculated from hull_angle and hull_position_0 so from an information point of view
# the ObservableState and the State are equivalent.
type ObservableState {
    hull_angle: number,
    hull_position_0: number,
    hull_position_1: number,
    hull_angularVelocity: number,
    vel_x: number,
    vel_y: number,
    hip_joint_1_angle: number,
    hip_joint_1_speed: number,
    hip_joint_1_motor_speed: number,
    knee_joint_1_angle: number,
    knee_joint_1_speed: number,
    knee_joint_1_motor_speed: number,
    leg_1_ground_contact_flag: number,
    hip_joint_2_angle: number,
    hip_joint_2_speed: number,
    hip_joint_2_motor_speed: number,
    knee_joint_2_angle: number,
    knee_joint_2_speed: number,
    knee_joint_2_motor_speed: number,
    leg_2_ground_contact_flag: number,
    game_over: number,
    lidar_0: number,
    lidar_1: number,
    lidar_2: number,
    lidar_3: number,
    lidar_4: number,
    lidar_5: number,
    lidar_6: number,
    lidar_7: number,
    lidar_8: number,
    lidar_9: number
}

type Action {
    hip_1: number<min_action..max_action>,
    knee_1: number<min_action..max_action>,
    hip_2: number<min_action..max_action>,
    knee_2: number<min_action..max_action>
}

type SimConfig {
    hip_1: number,
    knee_1: number,
    hip_2: number,
    knee_2: number
}

function Reward(obs: State, act: Action) {
    if obs.game_over or obs.hull_position_0 < 0 {
        return -100
    } else if obs.hull_position_0 > (TERRAIN_LENGTH-TERRAIN_GRASS)*TERRAIN_STEP {
        return 500
    } else {
        var shaping = 130*obs.hull_position_0/SCALE  # moving forward is a way to receive reward (normalized to get 300 on completion)
        shaping = shaping - 5.0*Math.Abs(obs.hull_angle)  # keep head straight, other than that and falling, any behavior is unpunished

        var r = shaping - obs.preview_shaping

        r = r - 0.00035 * MOTORS_TORQUE * Math.Min(Math.Max(Math.Abs(act.hip_1), 0),1)
        r = r - 0.00035 * MOTORS_TORQUE * Math.Min(Math.Max(Math.Abs(act.knee_1), 0),1)
        r = r - 0.00035 * MOTORS_TORQUE * Math.Min(Math.Max(Math.Abs(act.hip_2), 0),1)
        r = r - 0.00035 * MOTORS_TORQUE * Math.Min(Math.Max(Math.Abs(act.knee_2), 0),1)

        if obs.hull_position_1 >= 5 {
            r = r + 0.1
        } else {
            r = r - 0.1
        }

        return r
    }
}

function Terminal(obs:State, act: Action) {
    return obs.game_over or obs.hull_position_0 < 0 or obs.hull_position_0 > (TERRAIN_LENGTH-TERRAIN_GRASS)*TERRAIN_STEP
}

graph (input: ObservableState): Action {
    concept walk_without_falling(input): Action {
        curriculum {
            source simulator (Action: Action, Config: SimConfig): State {
            }

            terminal Terminal
            reward Reward

            lesson `Initial config` {
                scenario {
                    hip_1: number<0.0>,
                    knee_1: number<0.0>,
                    hip_2: number<0.0>,
                    knee_2: number<0.0>
                }
            }

            training {
                # Iterations per episode 2000
                EpisodeIterationLimit: 2000,
                # Finish the training when the brain doesn't progress for 500000 iterations.
                NoProgressIterationLimit: 2000000
            }
        }
    }
}
