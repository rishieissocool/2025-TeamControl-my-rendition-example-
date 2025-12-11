import math
import numpy as np

from TeamControl.network.robot_command import RobotCommand
from TeamControl.world.model import WorldModel as wm
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot.Movement import RobotMovement


def go_to_ball_and_shoot(world_model: wm, isYellow: bool, robot_id: int):
    # 1. Get ball and robot pose from the world model
    ball = world_model.get_ball()
    robot_pos = world_model.get_robot(isYellow=isYellow, robot_id=robot_id)

    if ball is None or robot_pos is None:
        return RobotCommand(robot_id=robot_id)

    ball_pos = (ball.x, ball.y)

    # 2. Work out which way WE are attacking
    try:
        us_positive = world_model.us_positive()
    except Exception:
        us_positive = True  # default: attack +x

    geom = world_model.geometry_data
    field = geom.field_size

    # Opponent goal: +x if we attack positive, else -x
    goal_x = field.field_length / 2.0 if us_positive else -field.field_length / 2.0
    goal_y = 0.0
    goal_pos = (goal_x, goal_y)

    # 3. Position where robot should stand to shoot
    shooting_pos = RobotMovement.shooting_pos(ball_pos, goal_pos, robot_offset=200.0)

    # 4. Velocity to go to that shooting position and face the opponent goal
    vx, vy, w = RobotMovement.velocity_to_target(
        robot_pos=robot_pos,
        target=shooting_pos,
        turning_target=goal_pos,
        stop_threshold=0
    )

    # 5. Kick decision
    ball_rel = world2robot(robot_position=robot_pos, target_position=ball_pos)
    dist_to_ball = math.hypot(ball_rel[0], ball_rel[1])

    goal_rel = world2robot(robot_position=robot_pos, target_position=goal_pos)
    angle_to_goal = math.atan2(goal_rel[1], goal_rel[0])

    close_enough = dist_to_ball < 120.0
    facing_goal = abs(angle_to_goal) < 0.15

    kick = 1 if (close_enough and facing_goal) else 0

    return RobotCommand(
        robot_id=robot_id,
        vx=vx,
        vy=vy,
        w=w,
        kick=kick,
        dribble=0
    )

