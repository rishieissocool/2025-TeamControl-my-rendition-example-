## legacy code 
from TeamControl.network import *

#from TeamControl.Examples.PathPlaner import pathplanning 
from TeamControl.world.model import World
from TeamControl.world.transform_cords import world2robot
from TeamControl.world.Trajectory import predict_trajectory
from old_stuff.voronoi_planner import VoronoiPlanner

from TeamControl.robot.Movement import RobotMovement

if __name__ == "__main__":
    # VARIABLES 
    us_yellow = False
    goalie_id = 2
    Player_id = 6
    us_positive = True
    goalie_ip = "192.168.110.108"
    player_ip = "192.168.110.243"
    robot_port = 50514
                # ball_pos = vision_sock.world_model.get_ball()
            # print(f"{ball_pos=}")
    world_model = World(isYellow=us_yellow,isPositive=us_positive)
    vision_sock = vision(world_model)
    sender1 = Sender(ip=goalie_ip,port=robot_port)
    sender2 = Sender(ip=player_ip,port=robot_port)
    
    planner = VoronoiPlanner(xsize=9000,ysize=6000)
    
    start_time = time.time()

        
    while True:     
        isUpdated = vision_sock.listen() # is the current detection frame updated ?
        if isUpdated and time.time() >= start_time + 0.1: # now the detection frame is fully updated
        # if isUpdated:
            # do operations
            ball_hist = vision_sock.world_model.get_ball(True)
            ball_pos = vision_sock.world_model.get_ball()
            print(f"{len(ball_hist)=}")
            golaie_points = predict_trajectory(ball_hist, 3, isPostive= us_positive, feild_size=(4800, 2700))
            
            golaie_pos = vision_sock.world_model.get_our_robot(robot_id=goalie_id)
            print(f"{golaie_pos=}")
            # target = ball_pos
            
            if golaie_points[1] == True:
                target_pos1 = world2robot(robot_position=golaie_pos,target_position=golaie_points[0])
            else:
                target_pos1 = world2robot(robot_position=golaie_pos,target_position= (2200, 0))
            print(f"{golaie_points=}")
            # points = pathplanning(planner,vision_sock.world_model,ball_p
            

            print("Relative Target : ", target_pos1)
            # target_pos = world2robot(robot_position=robot_pos,target_position=target)
            # # print(target)
            vx1,vy1 = RobotMovement.go_To_Target(target_pos=target_pos1, stop_threshold=50)
            # w1 = RobotMovement.turn_to_target(target_pos2)
            # w = 0 
    
            action1 = Action(robot_id=goalie_id,vx=vx1*40,vy=vy1*40)
            
            
            player_pos = vision_sock.world_model.get_our_robot(robot_id=Player_id)
            print(f"{player_pos=}")
            # target = ball_pos
            
            target_pos2 = world2robot(robot_position=player_pos,target_position=ball_pos)
            print("Relative Target : ", target_pos2)
            # target_pos = world2robot(robot_position=robot_pos,target_position=target)
            # # print(target)
            vx2,vy2 = RobotMovement.go_To_Target(target_pos=target_pos2)
            
            action2 = Action(robot_id=goalie_id,vx=vx2*40,vy=vy2*40)
            # # print(action)   
            sender1.send_action(action=action1,destination=(goalie_ip,robot_port))
            sender2.send_action(action=action2,destination=(player_ip,robot_port))
            
            start_time = time.time()
    
    
    