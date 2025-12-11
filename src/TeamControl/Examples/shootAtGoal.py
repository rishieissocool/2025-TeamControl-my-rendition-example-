import math
from TeamControl.network.robot_command import RobotCommand
from TeamControl.world.model import WorldModel as wm
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot.Movement import RobotMovement

# Make sure these match striker.py
APPROACH_RADIUS    = 300.0    # mm
ALIGN_TOL          = 0.15     # rad (~8.5°)
KICK_DISTANCE      = 120.0    # mm
ROBOT_OFFSET       = 200.0    # mm
FALLBACK_FIELD_LEN = 9000.0   # mm


def go_to_ball_and_shoot(world_model: wm, isYellow: bool, robot_id: int) -> RobotCommand:
    """
    Single-step version of run_striker:
    - If far from ball: go to a point behind the ball on ball→goal line, facing the goal.
    - If close: stop translating, only rotate to face goal.
    - Kick when close to ball AND aligned with goal.
    """

    # 1) Get latest frame
    frame = world_model.get_latest_frame()
    if frame is None:
        # No vision → stop
        return RobotCommand(robot_id=robot_id)

    # 2) Get ball
    ball = frame.ball
    if ball is None:
        return RobotCommand(robot_id=robot_id)

    ball_pos = (float(ball.x), float(ball.y))

    # 3) Get our robot
    try:
        robot = frame.get_yellow_robots(isYellow=isYellow, robot_id=robot_id)
    except Exception:
        robot = None

    if robot is None or robot.position is None:
        return RobotCommand(robot_id=robot_id)

    # robot.position is np.array([x, y, theta])
    robot_pose = robot.position
    robot_pos_tuple = (
        float(robot_pose[0]),
        float(robot_pose[1]),
        float(robot_pose[2]),
    )

    # 4) Which way are WE attacking? (same logic as run_striker)
    try:
        us_positive = world_model.us_positive()
    except Exception:
        us_positive = True  # fallback

    # Field length (geometry if available, else fallback)
    field_len = FALLBACK_FIELD_LEN
    if getattr(world_model, "field", None) is not None:
        try:
            field_len = float(world_model.field.field_length)
        except Exception:
            pass

    goal_x = (field_len / 2.0) * (1.0 if us_positive else -1.0)
    goal_y = 0.0
    goal_pos = (goal_x, goal_y)

    # 5) Ball & goal in robot frame
    ball_rel = world2robot(robot_pose, ball_pos)
    goal_rel = world2robot(robot_pose, goal_pos)

    dist_to_ball = math.hypot(ball_rel[0], ball_rel[1])
    angle_to_goal = math.atan2(goal_rel[1], goal_rel[0])

    # ==================================================
    # MODE 2: CLOSE-RANGE ALIGNMENT & SHOOT (same as run_striker)
    # ==================================================
    if dist_to_ball < APPROACH_RADIUS:
        vx = 0.0
        vy = 0.0

        if abs(angle_to_goal) > ALIGN_TOL:
            w = 3.0 * math.copysign(1.0, angle_to_goal)
        else:
            w = 0.0

        # Kick only if close & aligned (same condition as run_striker)
        if dist_to_ball < KICK_DISTANCE and abs(angle_to_goal) < ALIGN_TOL:
            kick = 1
        else:
            kick = 0

    # ==================================================
    # MODE 1: APPROACH BEHIND BALL (same as run_striker)
    # ==================================================
    else:
        shooting_pos = RobotMovement.shooting_pos(
            ball_pos=ball_pos,
            shootingTarget=goal_pos,
            robot_offset=ROBOT_OFFSET,
        )

        vx, vy, w = RobotMovement.velocity_to_target(
            robot_pos=robot_pos_tuple,
            target=shooting_pos,
            turning_target=goal_pos,
            stop_threshold=150.0,
        )

        kick = 0  # never kick in approach mode

    # 6) Return the command (no queue here, just one step)
    return RobotCommand(
        robot_id=robot_id,
        vx=vx,
        vy=vy,
        w=w,
        kick=kick,
        dribble=0,
    )
