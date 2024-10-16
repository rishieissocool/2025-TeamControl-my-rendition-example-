from TeamControl.VoronoiPlanner.VoronoiPlanner import VoronoiPlanner
from TeamControl.Model.world import World
from TeamControl.Model.frame import Robot as r

import time
import numpy as np

x = 9000 
y = 6000
# planner = VoronoiPlanner(xsize=x,ysize=y)

def pathplanning(planner:VoronoiPlanner,world_model:World,target_pos):
    """
    This generates waypoints for all of our robots to target and returns as a list

    Args:
        planner (VoroniPlanner): the initialised Planner.
        world_model (World): World Model from vision socket
        target_pos (tuple[float,float]): targeted location e.g. ball_pos 

    Returns:
        list: list of waypoints (order by robot_id)
    """
    # planner = VoronoiPlanner(xsize=x,ysize=y) # not recommended

    CLEARANCE = 10
    d0 = 10
    N = 100
    
    start:r = world_model.get_our_robot(robot_id=None,format=r.XY)
    our_robots:list = world_model.get_our_robot(robot_id=None,format=r.OBS)
    enemy_robots:list = world_model.get_enemy_robot(robot_id=None, format=r.OBS)
    obstacles:list = our_robots + enemy_robots
    goals = [target_pos,target_pos,target_pos,target_pos,target_pos,target_pos]

    print("number of Obstacles:",len(obstacles))

    start_time = time.time()
    
    planner.update_obstacles(obstacles)

    initial_waypoints= planner.generate_waypoints(our_robots,goals,d0)
    waypoints = [planner.simplify([s] + w + [g], CLEARANCE, [o.unum()]) for s,w,g,o in zip(start,initial_waypoints,goals,obstacles)]

    end_time = time.time()
    excution_time = end_time - start_time
    print(f"{excution_time=}")

    print(f"final {waypoints=}")
    return waypoints

