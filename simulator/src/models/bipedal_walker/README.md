# Bipedal walker

## Objective

Get a 2D biped walker to walk through rough terrain.


## States

| Num	| Observation	             |  Min | Max  | Mean |
| ----- | -------------------------- | ---- | ---- | ---- |
| 0	    | hull_angle	             | 0	| 2*pi | 0.5  |
| 1	    | hull_angularVelocity	     | -inf	| +inf | -    |
| 2	    | vel_x	                     | -1	| +1   | -    |
| 3	    | vel_y	                     | -1	| +1   | -    |
| 4	    | hip_joint_1_angle	         | -inf	| +inf | -    |
| 5	    | hip_joint_1_speed	         | -inf	| +inf | -    |
| 6	    | knee_joint_1_angle	     | -inf	| +inf | -    |
| 7	    | knee_joint_1_speed	     | -inf	| +inf | -    |
| 8	    | leg_1_ground_contact_flag	 | 0	| 1	   | -    |
| 9	    | hip_joint_2_angle	         | -inf	| +inf | -    |
| 10	| hip_joint_2_speed	         | -inf	| +inf | -    |
| 11	| knee_joint_2_angle	     | -inf	| +inf | -    |
| 12	| knee_joint_2_speed	     | -inf	| +inf | -    |
| 13	| leg_2_ground_contact_flag	 | 0	| 1	   | -    |
| 14-23	| 10 lidar readings	         | -inf	| +inf | -    |



## Actions

Actions
Type: Box(4) - Torque control(default) / Velocity control

| State                       | Range         |
| --------------------------- | ------------- |
| Hip_1 (Torque / Velocity)   | [-1..1]   |
| Knee_1 (Torque / Velocity)  | [-Inf..Inf]   |
| Hip_2 (Torque / Velocity)   | [-41.8..41.8] |
| Knee_2 (Torque / Velocity)  | [-Inf..Inf]   |

## Configuration Parameters

Starting State
Random position upright and mostly straight legs.

| State                       | Range         |
| --------------------------- | ------------- |
| Hip_1 (Torque / Velocity)   | [0]           |
| Knee_1 (Torque / Velocity)  | [0]           |
| Hip_2 (Torque / Velocity)   | [0]           |
| Knee_2 (Torque / Velocity)  | [0]           |

Reward
Reward is given for moving forward, total 300+ points up to the far end. If the robot falls, it gets -100. Applying motor torque costs a small amount of points, more optimal agent will get better score. State consists of hull angle speed, angular velocity, horizontal speed, vertical speed, position of joints and joints angular speed, legs contact with ground, and 10 lidar rangefinder measurements. There's no coordinates in the state vector.

Episode Termination
The episode ends when the robot body touches ground or the robot reaches far right side of the environment.
