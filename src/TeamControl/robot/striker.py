import time
import math

from TeamControl.network.robot_command import RobotCommand
from TeamControl.world.model import WorldModel
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot.Movement import RobotMovement

# Tunable parameters
APPROACH_RADIUS = 300.0    # mm: when closer than this, stop moving & only rotate
ALIGN_TOL = 0.15           # rad (~8.5°): how close to goal direction is "aligned"
KICK_DISTANCE = 120.0      # mm: how close to ball before we allow a kick
ROBOT_OFFSET = 200.0       # mm: how far behind the ball to stand before shooting
FALLBACK_FIELD_LEN = 9000.0  # mm: used if geometry/field not yet set


def run_striker(dispatch_q,
                wm: WorldModel,
                robot_id: int = 0,
                is_yellow: bool = True):
    """
    Striker behaviour:
    - From far: move to a point behind the ball on the ball→goal line, facing the goal
    - From close: stop translating, only rotate toward the goal
    - Kick when close to the ball AND aligned with the goal
    """

    while True:
        # 1) Get the latest frame from world model
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

        ball_pos = (float(ball.x), float(ball.y))

        # 3) Get our robot from this frame
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

        # robot.position is expected to be np.array([x, y, theta])
        robot_pose = robot.position
        robot_pos_tuple = (
            float(robot_pose[0]),
            float(robot_pose[1]),
            float(robot_pose[2]),
        )

        # 4) Decide which direction we are attacking
        try:
            us_positive = wm.us_positive()
        except Exception:
            us_positive = True  # fallback if method not there

        # Try to get real field length from geometry; otherwise, fallback
        field_len = FALLBACK_FIELD_LEN
        if getattr(wm, "field", None) is not None:
            try:
                field_len = float(wm.field.field_length)
            except Exception:
                pass

        goal_x = (field_len / 2.0) * (1.0 if us_positive else -1.0)
        goal_y = 0.0
        goal_pos = (goal_x, goal_y)

        # 5) Compute ball & goal positions in robot frame
        ball_rel = world2robot(robot_pose, ball_pos)
        goal_rel = world2robot(robot_pose, goal_pos)

        dist_to_ball = math.hypot(ball_rel[0], ball_rel[1])
        angle_to_goal = math.atan2(goal_rel[1], goal_rel[0])

        # ==================================================
        # MODE 2: CLOSE-RANGE ALIGNMENT & SHOOT
        # ==================================================
        if dist_to_ball < APPROACH_RADIUS:
            # Stop translating, only rotate toward goal
            vx = 0.0
            vy = 0.0

            if abs(angle_to_goal) > ALIGN_TOL:
                # rotate toward goal
                w = 3.0 * math.copysign(1.0, angle_to_goal)
            else:
                w = 0.0

            # Kick only if close & aligned
            if dist_to_ball < KICK_DISTANCE and abs(angle_to_goal) < ALIGN_TOL:
                kick = 1
            else:
                kick = 0

            print(
                f"[STRIKER] CLOSE RANGE: dist={dist_to_ball:.1f}, "
                f"angle={angle_to_goal:.2f}, w={w:.2f}, kick={kick}"
            )

        # ==================================================
        # MODE 1: APPROACH BEHIND BALL
        # ==================================================
        else:
            # Compute a spot behind the ball along the ball→goal line
            shooting_pos = RobotMovement.shooting_pos(
                ball_pos=ball_pos,
                shootingTarget=goal_pos,
                robot_offset=ROBOT_OFFSET,
            )

            # Move toward that spot while turning to face the goal
            vx, vy, w = RobotMovement.velocity_to_target(
                robot_pos=robot_pos_tuple,
                target=shooting_pos,
                turning_target=goal_pos,
                stop_threshold=150.0,
            )

            kick = 0  # never kick in approach mode

            print(
                f"[STRIKER] APPROACH: dist={dist_to_ball:.1f}, "
                f"vx={vx:.2f}, vy={vy:.2f}, w={w:.2f}"
            )

        # 6) Build and send the command
        cmd = RobotCommand(
            robot_id=robot_id,
            vx=vx,
            vy=vy,
            w=w,
            kick=kick,
            dribble=0,
        )

        # Queue expects (command, runtime_in_seconds)
        dispatch_q.put((cmd, 0.1))

        # Run this loop at ~50 Hz
        time.sleep(0.02)
