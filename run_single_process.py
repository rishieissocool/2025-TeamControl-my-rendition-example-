from TeamControl.Network.ssl_networking import *
from TeamControl.Examples.PathPlaner import pathplanning 
from TeamControl.Model.world import World


if __name__ == "__main__":
    # VARIABLES 
    us_yellow = True
    id = 0
    us_positive = True
    isGrSimActive = True
    isVisionActive = False
    UseGrSimVision = True
    numRobotsActive = 0
    
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
        list_action = list()
    
        isUpdated = vision_sock.listen() # is the current detection frame updated ? 
        
        if isUpdated: # now the detection frame is fully updated
            # do operations
            ball_pos = vision_sock.world_model.get_ball()
            points = pathplanning(vision_sock.world_model,ball_pos)
            
            # if isGrSimActive:
            #     g_sender.send_action(isYellow=us_yellow,action=action)
            if numRobotsActive > 0:
                ...
    