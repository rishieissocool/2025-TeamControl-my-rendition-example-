from TeamControl.Network.ssl_networking import *
from TeamControl.Examples.PathPlaner import pathplanning 
from TeamControl.RobotBehaviour.Movement import RobotMovement 
from TeamControl.Model import world2robot
from TeamControl.Model.world import World
from TeamControl.VoronoiPlanner.VoronoiPlanner import VoronoiPlanner


if __name__ == "__main__":
    # VARIABLES 
    us_yellow = True
    robot_id = 0
    us_positive = True
    isGrSimActive = True
    isVisionActive = False
    UseGrSimVision = True
    numRobotsActive = 0
    planner = VoronoiPlanner(xsize=9000,ysize=6000)
    
    world_model = World(isYellow=us_yellow,isPositive=us_positive)
    if UseGrSimVision:
        world_model.max_cameras = 4
        # logging.info(f"Cameras Active : {world_model.max_cameras}")
        vision_sock = grSimVision(world_model=world_model)
    else:
        vision_sock = vision(world_model=world_model)
    
    if isGrSimActive:
        g_sender = grSimSender(ip="127.0.0.1")
    
    if numRobotsActive > 0 : 
        # interface show all active robots and where 
        print("expecting robots active :",numRobotsActive)
        sender = Sender(binding=True)
        b_sender = Broadcaster()
        ...
        
    while True: 
        list_command = list()
    
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
                vx,vy = RobotMovement.go_To_Target(target_pos=target_pos)
                w = RobotMovement.turn_to_target(target_pos,speed=2)
        
                Command = Command(robot_id=robot_id,vx=vx,vy=vy,w=w)
                print(Command)   
                if isGrSimActive:
                    g_sender.send_command(isYellow=us_yellow,Command=Command)
                if numRobotsActive > 0:
                    ...
    