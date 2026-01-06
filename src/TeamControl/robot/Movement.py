import math
import numpy as np
from typing import Tuple, Optional, List

from TeamControl.world.transform_cords import world2robot
from TeamControl.network.robot_command import RobotCommand


class RobotMovement:

    @classmethod
    def velocity_to_target(cls,robot_pos: tuple[float, float, float],
                           target: tuple[float,float], 
                           turning_target:tuple[float, float] = None,
                           speed: float = 0.01
                           , stop_threshold = 150) -> tuple[float, float, float]: 
        '''
        Gets the velocity required for the robot go to position and trun to target
        '''
        if robot_pos is None:
            print("Robot pos is none")
            pass
        
        transTarget = world2robot(robot_pos, target)
        vx, vy = cls.go_To_Target(transTarget, stop_threshold = stop_threshold,speed=speed)
        if turning_target is None:
            w = 0.0
        else:
            trans_turn_target = world2robot(robot_pos, turning_target)
            w = cls.turn_to_target(trans_turn_target)

        return vx, vy, w

    @staticmethod
    def turn_to_target(target:tuple[float,float] =None, epsilon: float=0.15, speed: float = 0.005, robotOmega = None):
        '''
            This function returns an agular velocity. The goal is to turn the robot
            in such a way that it is facing the ball with its kicker side.

            input: 
                ball_position: ball position in the robot coordinate systen (e.g. (10mm,50mm))
                epsilon: Threshold for the orientation (orientation does not have to be zero to 
                        consider it correct -> avoids jitter)
        '''
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
        d = math.sqrt(dx**2 + dy**2) # is this dx2/dx**2
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