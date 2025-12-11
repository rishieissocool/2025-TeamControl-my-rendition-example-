import math
import numpy as np
from typing import Tuple, Optional, List

from TeamControl.world.transform_cords import world2robot
from TeamControl.network.robot_command import RobotCommand


class RobotMovement:

    @classmethod
    def velocity_to_target(
        cls,
        robot_pos: tuple[float, float, float],
        target: tuple[float, float],
        turning_target: tuple[float, float] | None = None,
        stop_threshold: float = 150.0
    ) -> tuple[float, float, float]:

        if robot_pos is None:
            return 0.0, 0.0, 0.0

        # Convert world target to robot frame
        trans_target = world2robot(robot_pos, target)
        vx, vy = cls.go_To_Target(trans_target, stop_threshold=stop_threshold)

        # If we have a turning target, rotate toward it
        if turning_target is None:
            w = 0.0
        else:
            trans_turn_target = world2robot(robot_pos, turning_target)
            w = cls.turn_to_target(trans_turn_target)

        return vx, vy, w

    @staticmethod
    def turn_to_target(
        target: tuple[float, float] | None = None,
        epsilon: float = 0.15,
        speed: float = 5.0,
    ) -> float:
        """
        Correct rotation controller.
        Robot frame:
          x_forward = target[0]
          y_left    = target[1]
        """
        if target is None:
            return 0.0

        # Correct orientation for robot coordinate frame
        angle = math.atan2(target[1], target[0])

        # Avoid jitter
        if abs(angle) < epsilon:
            omega = 0.0
        elif abs(angle) < 2 * epsilon:
            omega = speed * math.copysign(0.05, angle)
        else:
            omega = speed * math.copysign(0.5, angle)

        return omega
    
    
    @staticmethod
    def behind_ball_point(ball, goal, buffer_radius):
        """
        ball  = (bx, by)
        goal  = (gx, gy)
        buffer_radius = distance of the behind-ball point from the ball

        Returns: (x, y) behind-ball target position
        """

        bx, by = ball
        gx, gy = goal

        # Direction vector from ball → goal
        dx = gx - bx
        dy = gy - by

        # Distance
        d = math.sqrt(dx2 + dy2)
        if d == 0:
            raise ValueError("Ball and goal cannot be at the same point")

        # Normalize direction
        dx /= d
        dy /= d

        # Opposite direction (behind the ball)
        behind_x = bx - dx * buffer_radius
        behind_y = by - dy * buffer_radius

        return behind_x, behind_y

    @staticmethod
    def go_To_Target(target_pos: tuple[float, float],
                     speed: float = 1.0,
                     stop_threshold: float = 150.0):

        if target_pos is None:
            return 0.0, 0.0

        dist = math.hypot(target_pos[0], target_pos[1])
        if dist > stop_threshold:
            vx = (target_pos[0] / dist) * speed
            vy = (target_pos[1] / dist) * speed
            return vx, vy

        return 0.0, 0.0

    @staticmethod
    def shooting_pos(ball_pos: tuple[float, float],
                     shootingTarget: tuple[float, float],
                     robot_offset: float = 200.0):

        direction = np.array(shootingTarget) - np.array(ball_pos)
        norm = np.linalg.norm(direction)

        if norm == 0:
            return np.array(ball_pos, dtype=float)

        direction /= norm
        return np.array(ball_pos) - robot_offset * direction
