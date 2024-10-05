from TeamControl.Network.Receiver import grSimVision
from TeamControl.VoronoiPlanner import *
from TeamControl.VoronoiPlanner.VoronoiPlanner import *
from TeamControl.Model.world import World as wm
from TeamControl.Model.frame import * 
from TeamControl.SSL.formationObs import *


def main():
    isYellow = True
    world_model = wm(isYellow=isYellow,isPositive=isYellow)
    vision = grSimVision(world_model)
    while world_model.field is None:
        vision.listen()
    while not world_model.is_detection_updated:
        vision.listen()
   
    start_time = time.time()

    x = world_model.field.field_length
    y = world_model.field.field_width
    
    our_robots:list = world_model.get_our_robot(robot_id=None,format=Robot.OBS)
    enemy_robots:list = world_model.get_enemy_robot(robot_id=None,format=Robot.OBS)
    
    all_obs = our_robots+enemy_robots
    
    print(all_obs)
    
    planner = VoronoiPlanner(x,y,all_obs)
    
    ## get target position (formation)
    formation_cords
    
    planner.generate_waypoints(our_robots,)
    execution_time = time.time()-start_time
    print(f"Execution time: {execution_time:.4f} seconds")
    
    
if __name__ =="__main__":
    main()