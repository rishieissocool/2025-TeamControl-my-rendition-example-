import time
import math

from TeamControl.network.robot_command import RobotCommand
from TeamControl.world.model import WorldModel
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot.Movement import RobotMovement


def run_striker(dispatch_q,
                wm: WorldModel,
                robot_id: int = 0,
                is_yellow: bool = True):
    """
    Real striker:
    - Reads latest frame from WorldModel
    - Finds ball + our robot
    - Moves to a point behind the ball along the goal line
    - Faces the opponent goal
    - Kicks when close & aligned
    """

    field_len = 9000.0  # mm fallback field length

    while True:
        # 1) Get the latest world-model frame
        try:
            frame = wm.get_latest_frame()
        except Exception as e:
            print("[STRIKER] get_latest_frame error:", e)
            time.sleep(0.02)
            continue

        if frame is None:
            print("[STRIKER] no frame yet")
            time.sleep(0.02)
            continue

        # 2) Get ball from frame
        ball = frame.ball
        if ball is None:
            print("[STRIKER] no ball in frame")
            time.sleep(0.02)
            continue

        ball_pos = (ball.x, ball.y)

        # 3) Get our robot (same API style as your PathPlanner)
        try:
            robot = frame.get_yellow_robots(isYellow=is_yellow, robot_id=robot_id)
        except Exception as e:
            print("[STRIKER] get_yellow_robots error:", e)
            time.sleep(0.02)
            continue

        if robot is None:
            print("[STRIKER] robot is None")
            time.sleep(0.02)
            continue

        robot_pose = robot.position  # np.array([x, y, o])
        robot_pos_tuple = (
            float(robot_pose[0]),
            float(robot_pose[1]),
            float(robot_pose[2]),
        )

        # 4) Decide which side we attack (positive or negative x)
        try:
            us_positive = wm.us_positive()
        except Exception:
            us_positive = True  # fallback if method not there

        goal_x = (field_len / 2.0) * (1 if us_positive else -1)
        goal_y = 0.0
        goal_pos = (goal_x, goal_y)

        # 5) Compute shooting position: behind the ball on line ball→goal
        shooting_pos = RobotMovement.shooting_pos(
            ball_pos=ball_pos,
            shootingTarget=goal_pos,
            robot_offset=200.0,   # how far behind the ball
        )

        # 6) Velocities to go to that pos and face the goal
        vx, vy, w = RobotMovement.velocity_to_target(
            robot_pos=robot_pos_tuple,
            target=shooting_pos,
            turning_target=goal_pos,
            stop_threshold=150.0,
        )

        # 7) Decide if we should kick now
        #    Ball in robot frame
        ball_rel = world2robot(robot_position=robot_pose, target_position=ball_pos)
        dist_to_ball = math.hypot(ball_rel[0], ball_rel[1])

        #    Goal in robot frame
        goal_rel = world2robot(robot_position=robot_pose, target_position=goal_pos)
        angle_to_goal = math.atan2(goal_rel[1], goal_rel[0])

        close_enough = dist_to_ball < 120.0       # mm threshold
        facing_goal  = abs(angle_to_goal) < 0.15  # ~8.5 degrees

        kick = 1 if (close_enough and facing_goal) else 0

        print(
            f"[STRIKER] dist={dist_to_ball:.1f}, angle={angle_to_goal:.2f}, "
            f"vx={vx:.2f}, vy={vy:.2f}, w={w:.2f}, kick={kick}"
        )

        cmd = RobotCommand(
            robot_id=robot_id,
            vx=vx,
            vy=vy,
            w=w,
            kick=kick,
            dribble=0,
        )

        # 8) Send command to dispatcher
        dispatch_q.put((cmd, 0.1))

        time.sleep(0.02)
