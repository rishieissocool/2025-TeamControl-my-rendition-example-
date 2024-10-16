from TeamControl.VoronoiPlanner.VoronoiPlanner import VoronoiPlanner
from TeamControl.Model.world import World
from TeamControl.Model.frame import Robot as r

import time
import numpy as np

x = 9000 
y = 6000
planner = VoronoiPlanner(xsize=x,ysize=y)

def pathplanning(world_model:World,target_pos):
    planner = VoronoiPlanner(xsize=x,ysize=y)

    CLEARANCE = 100
    d0 = 10
    N = 11 
    ball = world_model.get_ball()
    
    # this_robot:r = world_model.get_our_robot(robot_id=robot_id,format=r.SELF)
    our_robots:list = world_model.get_our_robot(robot_id=None,format=r.OBS)
    enemy_robots:list = world_model.get_enemy_robot(robot_id=None, format=r.OBS)
    obstacles:list = our_robots + enemy_robots
    # obstacles.remove(this_robot.obs)
    goals = [target_pos,target_pos,target_pos,target_pos,target_pos,target_pos]

    print("number of Obstacles:",len(obstacles))
    print(f"{our_robots=}")
    print(f"{goals=}")
    centres = np.vstack([o.centre() for o in obstacles])

    start_time = time.time()
    
    planner.update_obstacles(obstacles)

    waypoints= planner.generate_waypoints(our_robots,goals,d0)
    # waypoints = [planner.simplify([s] + w + [g], CLEARANCE, [o.unum()]) for s,w,g,o in zip(starts,initial_waypoints,goals,obstacles)]

    end_time = time.time()
    excution_time = end_time - start_time
    print(f"{excution_time=}")

    print(f"{waypoints=}")
    return waypoints

