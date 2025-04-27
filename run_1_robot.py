from TeamControl.network import Vision,Sender,RobotCommand

from TeamControl.examples.PathPlaner import pathplanning 
from TeamControl.world.main import WorldModel as wm
from TeamControl.world.transform_cords import world2robot
from TeamControl.voronoi_planner.voronoi_planner import VoronoiPlanner

from TeamControl.robot_behaviour.Movement import RobotMovement

import time

if __name__ == "__main__":
    # VARIABLES 
    us_yellow = True
    robot_id = 1
    us_positive = True
    robot_ip = "192.168.8.200"
    robot_port = 50514
    world_model = wm(isYellow=us_yellow,isPositive=us_positive)
    vision_sock = Vision(world_model)
    sender = Sender(ip=robot_ip,port=robot_port)
    planner = VoronoiPlanner(xsize=9000,ysize=6000)
    
    start_time = time.time()

        
    while True:     
        isUpdated = vision_sock.listen() # is the current detection frame updated ?
        if isUpdated and time.time() >= start_time + 0.05: # now the detection frame is fully updated
        # if isUpdated:
            # do operations
            ball_pos = vision_sock.world_model.get_ball()
            # print(f"{ball_pos=}")
            # points = pathplanning(planner,vision_sock.world_model,ball_pos)
            
            robot_pos = vision_sock.world_model.get_our_robot(robot_id=robot_id)
            print(f"{robot_pos=}")
            # target = ball_pos
            
            target_pos = world2robot(robot_position=robot_pos,target_position=ball_pos)
            print("Relative Target : ", target_pos)
            # target_pos = world2robot(robot_position=robot_pos,target_position=target)
            # # print(target)
            vx,vy = RobotMovement.go_To_Target(target_pos=target_pos)
            # w = RobotMovement.turn_to_target(target_pos)
            # w = 0 
    
            cmd = RobotCommand(robot_id=robot_id,vx=vx*20,vy=vy*20)
            # print(Command)   
            sender.send_command(Command=cmd,destination=(robot_ip,robot_port))
            
            start_time = time.time()
    