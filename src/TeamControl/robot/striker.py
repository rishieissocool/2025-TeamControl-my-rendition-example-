import time

from TeamControl.network.robot_command import RobotCommand


def run_striker(dispatch_q, wm, robot_id: int = 0, is_yellow: bool = True):
    """
    TEST VERSION: ignore world model, just drive forward.
    """
    while True:
        cmd = RobotCommand(
            robot_id=robot_id,
            vx=1.0,   # forward
            vy=0.0,
            w=0.0,
            kick=0,
            dribble=0,
        )

        print("[STRIKER TEST] sending constant forward command")
        dispatch_q.put((cmd, 0.1))
        time.sleep(0.02)