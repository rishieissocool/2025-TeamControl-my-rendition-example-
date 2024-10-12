from TeamControl.Network.ssl_networking import *
from TeamControl.Model.world import World

if __name__ == "__main__":
    # VARIABLES 
    isYellow = True
    isPositive = True
    isGrSimActive = True
    isVisionActive = False
    UseGrSimVision = True
    numRobotsActive = 0
    
    world_model = World(isYellow=isYellow,isPositive=isYellow)
    if UseGrSimVision:
        world_model.max_cameras = 4
        # logging.info(f"Cameras Active : {world_model.max_cameras}")
        vision_sock = grSimVision(world_model=world_model)
    else:
        vision_sock = vision(world_model=world_model)
    
    if isGrSimActive:
        g_sender = grSimSender(ip="127.0.0.1")
    
    if numRobotsActive > 0 : 
        print("expecting robots active :",numRobotsActive)
        sender = Sender(binding=True)
        b_sender = Broadcaster()
        ...
        
    while True: 
        list_action = list()
    
        isUpdated = vision_sock.listen()
        if isUpdated:
            ball_pos = vision_sock.world_model.get_ball()
            print(f"{ball_pos=}")
            action = RobotAction(robot_id=0,vx=1,vy=1)
            if isGrSimActive:
                g_sender.send_action(isYellow=isYellow,action=action)
            if numRobotsActive > 0:
                ...
    