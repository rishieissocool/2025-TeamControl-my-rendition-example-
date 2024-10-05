import time
'''
THIS HAS BEEN MOVED TO BEHAVIOUR.PY
'''
from TeamControl.Model.transform_cords import *
import math
import numpy as np
c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)


def turn_to_target(target:tuple[float,float], epsilon: float=0.15, speed: float = 5.0):
    '''
        This function returns an agular velocity. The goal is to turn the robot
        in such a way that it is facing the ball with its kicker side.

        input: 
            ball_position: ball position in the robot coordinate systen (e.g. (10mm,50mm))
            epsilon: Threshold for the orientation (orientation does not have to be zero to 
                     consider it correct -> avoids jitter)
    '''
    if target is None:
        return 0
    orientation_to_ball = np.arctan2(target[0], target[1])-np.pi/2

    if abs(orientation_to_ball) < epsilon:
        # to avoid jitter
        omega = 0
    elif abs(orientation_to_ball) > epsilon and abs(orientation_to_ball) < 4*epsilon:
        omega = -speed*np.sign(orientation_to_ball) * 0.5
    else:
        omega = -speed*np.sign(orientation_to_ball)
    return omega 

def go_To_Target(target_pos: tuple[float,float], speed: int=1, stop_threshold:float=150):
    """go To Target Position (in respect to Robot)
    if the distance is further away from stop_threshold,
    it will go to target position with calculated speed.

    Args:
        target_pos (tuple[float,float]): targeted position relative to robot
        speed (int, optional): Speed of Robot going to target. Defaults to 5.
        stop_threshold (float, optional): Distance range for robot to ignore. Defaults to 300.

    Returns:
        tuple[float,float]: velcocity x , velocity y
    """
    if target is None:
        return 0,0
    distance = math.sqrt(target_pos[0]**2 + target_pos[1]**2)

    # print(distance)
    if distance > stop_threshold:
        vy:float = (target_pos[1] / distance) * speed
        vx:float = (target_pos[0] / distance) * speed
        return vx,vy
    else: 
        return 0,0


if __name__ == '__main__':
    from TeamControl.shared.Action import Action
    from TeamControl.Coms.grSimAction import grSim_Action

    from TeamControl.Network.Receiver import grSimVision,vision
    from TeamControl.Network.Sender import robotSender,grSimSender
    from TeamControl.Model.world import World as wm
    print("is OUR Team Color YELLOW ? 1. YES 2. NO ")
    i = int(input())
    if i == 1 :
        isYellow = True
    else :
        isYellow = False
    world_model = wm(isYellow=isYellow,isPositive=isYellow)
    print("Are you using grSim 1.YES 2.NO")
    isgrSim = int(input())
    
    if isgrSim==1:
        receiver = grSimVision(world_model)
        sender = grSimSender()

    else:
        receiver = vision(world_model)
        sender = robotSender()

    while True:
        updated = receiver.listen()
        if updated is True :
            # obtain target
            target = world_model.get_ball()
            robot_id = 1
            pos = world_model.get_our_robot(robot_id)
            tag = world2robot(pos, target)
            print(f"{tag=}")
            vx,vy = go_To_Target(tag)
            w = turn_to_target(tag)
            if isgrSim==1:
                action = grSim_Action(isYellow,robot_id,vx,vy,w)
            else:
                action = Action(robot_id,vx,vy,w)
            print(action)
            # sends action to robot
            sender.send_action(action)