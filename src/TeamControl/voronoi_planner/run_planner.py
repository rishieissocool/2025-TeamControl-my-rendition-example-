from TeamControl.voronoi_planner.planner import VoronoiPlanner
from TeamControl.world.model import WorldModel as wm
import time

class PathPlanner():
    # values are from before.
    CLEARANCE = 200
    d0 = 250
    N = 100
    
    def __init__(self,world_model:wm,planner_q):
        self.isYellow = True
        self.version = 0
        self.wm = world_model
        field_x, field_y = (9000,6000)
        self.p = VoronoiPlanner(xsize=field_x,ysize=field_y) #initialise planner
        self.output_q = planner_q # output to behaviour tree or world model
        
    def check_wm_update(self):
    #get update from world model
        # updates from world model if this is active
        self.isYellow = self.wm.us_yellow() if hasattr(self.wm, "us_yellow") else self.isYellow 
        
        # frame version check. 
        new_version = self.wm.get_version() #compares version
        if self.version < new_version:
            self.version = new_version
            self.frame = self.wm.get_latest_frame() #updates the frame
            return True
        return False
                
    def running (self):
        ## this is for multi processing usage
        robot_id = 0  # example for robot 0
        while True:
            is_updated = self.check_wm_update()
            # follow waypoints here 
            if is_updated is True:
                target_pos = self.frame.ball.position # or some position
                waypoints:list = self.pathplanning(robot_id=robot_id,target_pos=target_pos)
                if isinstance(waypoints, list): # if the waypoint exists
                    # push forward waypoints to output (back to world model / behaviour tree)
                    self.output_q.put((robot_id,waypoints))  


    ## this is modified from the example, and I turned it into 1 robot only.
    def pathplanning(self,robot_id,target_pos):
        """
        This generates waypoints for all of our robots to target and returns as a list

        Args:
            robot_id (int): id of robot to plan for
            target_pos (tuple[float,float]): targeted location e.g. ball_pos 

        Returns:
            list: list of waypoints (for this robot_id)
        """
        # planner = VoronoiPlanner(xsize=x,ysize=y) # not recommended

        # the start positions of our robots
        start = [self.frame.get_yellow_robots(isYellow=self.isYellow,robot_id=robot_id)]
        # obstacles
        our_robot_obs = [r.obstacle for r in self.frame.get_our_robots(us=True, robot_id=None)]
        enemy_robot_obs = [r.obstacle for r in self.frame.get_our_robots(us=False, robot_id=None)]
        obstacles = our_robot_obs + enemy_robot_obs
        # the destination point of these
        goals = [target_pos]
        print("number of Obstacles:",len(obstacles))

        start_time = time.time()
        
        self.p.update_obstacles(obstacles)

        initial_waypoints= self.p.generate_waypoints(start,goals,self.d0)
        waypoints = [self.p.simplify([s] + w + [g], self.CLEARANCE, [o.unum()]) for s,w,g,o in zip(start,initial_waypoints,goals,obstacles)]

        end_time = time.time()
        excution_time = end_time - start_time
        print(f"{excution_time=}")

        print(f"final {waypoints=}")
        return waypoints

def run_planner(world_model:wm,planner_q):
    planner = PathPlanner(world_model,planner_q)
    planner.running()