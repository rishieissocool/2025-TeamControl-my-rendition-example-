from TeamControl.prm import *
from TeamControl.RobotBehaviour.goToTarget import go_To_Target, turn_to_target
from TeamControl.Model.transform_cords import world2robot
from TeamControl.shared.Action import Action
from TeamControl.Model.world import World as wm
from TeamControl.Network.Receiver import *
from TeamControl.Network.Sender import *
from TeamControl.Coms.grSimAction import grSim_Action
import math
isYellow = False
def main():
    world_model = wm(isYellow)
    print("are you using grSim ? 1. Yes  2. No")
    isgrSim = int(input())
    if isgrSim==1:
        receiver = grSimVision(world_model)
        sender = grSimSender()
    else:
        receiver = vision(world_model)
        sender = robotSender()
    print("Pick a robot ID")
    this_robot_id = int(input())
    while True:
        updated = receiver.listen()    
        if updated is True: 
            point = world_model.get_ball()
            x,y,o = world_model.get_our_robot(this_robot_id)
            robot_pos = [x,y]
            all_obs = []
            sample = 20
            robot_id_list = [0,1]
            wayPoint = None
            # field_w = getattr(world_model,"field_width")
            # field_l = getattr(world_model,"field_length")
            field_w = 6000
            field_l = 9000
            for id in robot_id_list:
                obs= world_model.get_enemy_robot(id,obs=True)
                if id != this_robot_id:
                    obs = world_model.get_our_robot(id,obs=True)
                all_obs.append(obs)
                print(all_obs)
            utils = Utils(x_min=-field_w/2,y_min=-field_l/2,x_max=field_w/2,y_max=field_l/2)
            x_min, y_min, x_max, y_max = utils.getBoundaries()
            print([x_min, y_min, x_max, y_max])
            prm  = PRMController(sample, all_obs, robot_pos, point)
            if prm.checkLineCollision((robot_pos[0], robot_pos[1]), (point[0], point[1])) is False: # No Collision
                new_point_pos = (point[0], point[1])
                wayPoint = None
                # print(new_point_pos)
                
            elif wayPoint is None or prm.checkLineCollision(robot_pos, wayPoint[1]):
            #sets the boundries
                prm.setBoundaries(x_min, y_min, x_max, y_max)
                initialRandomSeed = 0
                #runs PRM assgines the realuting list to pointsToEnd
                pointsToEnd, dist = prm.runPRM(initialRandomSeed, saveImage= False)
                if dist == None:
                    pointsToEnd = [(robot_pos[0], robot_pos[1]),(point[0], point[1])]
                    # copyes the points to waypoint 
                    # assgines the next point to move to as new point
                wayPoint = pointsToEnd.copy()
                new_point_pos = pointsToEnd[1]
                # print(new_point_pos)
            else:
                # makes sure that way point is assgined to new point 
                new_point_pos = wayPoint[1]
                distance_x = new_point_pos[0] - robot_pos[0]
                distance_y = new_point_pos[1] - robot_pos[1]
                # checks if the distance between the new points is greater than 2500
                if (math.pow(distance_x,2) + math.pow(distance_y,2)) > 2500:
                    #if it is we delete the way point 
                    del wayPoint[1]
                    
            trans_target = np.array(new_point_pos)
            # print(trans_target)
            # works
            tag = world2robot((x,y,o),(trans_target[0],trans_target[1]))
            # print(f"{tag=}")
            w = turn_to_target(tag)
            vx,vy = go_To_Target(tag)
            action = grSim_Action(isYellow,this_robot_id,vx,vy,w)
            # print(action)
            # sends action to robot1
            sender.send_action(action)

if __name__ == "__main__":
   
    main()








        

    
    

    

