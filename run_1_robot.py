from TeamControl.Network.Sender import Sender
from TeamControl.Network.ssl_networking import *

from TeamControl.Examples.PathPlaner import pathplanning 
from TeamControl.Model import World, world2robot
from TeamControl.VoronoiPlanner.VoronoiPlanner import VoronoiPlanner

from TeamControl.RobotBehaviour.Movement import RobotMovement

if __name__ == "__main__":
    # VARIABLES 
    us_yellow = True
    robot_id = 0
    us_positive = True
    robot_ip = ""
    robot_port = 50514
    
    world_model = World(isYellow=us_yellow,isPositive=us_positive)
    vision_sock = vision(world_model)
    sender = Sender(ip=robot_ip,port=robot_port)
    planner = VoronoiPlanner(xsize=9000,ysize=6000)
    
   
        
    while True:     
        isUpdated = vision_sock.listen() # is the current detection frame updated ?
        if isUpdated: # now the detection frame is fully updated
            # do operations
            ball_pos = vision_sock.world_model.get_ball()
            points = pathplanning(planner,vision_sock.world_model,ball_pos)
            for robot_id in vision_sock.world_model.get_our_ids():
                robot_pos = vision_sock.world_model.get_our_robot(robot_id=robot_id)
                target = points[robot_id][1]
                target_pos = world2robot(robot_position=robot_pos,target_position=target)
                # print(target)
                vx,vy = RobotMovement.go_To_Target(target_pos=target)
                w = RobotMovement.turn_to_target(target_pos,speed=2)
        
                action = Action(robot_id=robot_id,vx=vx,vy=vy,w=w)
                print(action)   
                sender.send_action(action=action,destination=(robot_ip,robot_port))
    