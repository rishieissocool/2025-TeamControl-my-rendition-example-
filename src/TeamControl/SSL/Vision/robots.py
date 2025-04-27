from TeamControl.voronoi_planner.obstacle import Obstacle

import numpy as np
import numpy.typing as npt 


class Robot:
    
    def __init__(self,robot_data,isYellow:bool) -> object:
        self.isYellow : bool = isYellow
        self.id : int = robot_data.robot_id
        self.c : float = robot_data.confidence
        self.x : float = robot_data.x
        self.y : float = robot_data.y
        self.o : float = robot_data.orientation
        self.px : float = robot_data.pixel_x
        self.py : float = robot_data.pixel_y
        
    @property
    def position(self) -> npt.ArrayLike:
        return np.array([self.x, self.y, self.o], dtype=np.float32)
    
    # def __lt__(self,other):
    #     return self.id < other.id
    
    @property
    def obstacle(self) -> Obstacle:
        # buffer = 250
        # top_left= [self.x-buffer, self.y+buffer]
        # bottom_right= [self.x+buffer, self.y-buffer]
        # return Obstacle(top_left, bottom_right)
    
        return Obstacle(point=(self.x,self.y),
                        radius=90,
                        unum=self.id,
                        isYellow=self.isYellow)    
    
    def __repr__(self):
        if self.isYellow is True:
            color = 'Yellow'
        elif self.isYellow is False:
            color = 'Blue'
        return f'''
    Team: {color} 
    Robot ID : {self.id} | Confidence : {self.c}
    position: {self.position} | PIXEL : {self.px}, {self.py} 
    OBS : {self.obstacle} 
    '''
        
        

class Team ():
    def __init__(self,team_robots:list, team_is_yellow:bool):
        self.isYellow : bool= team_is_yellow
        self.num_robots:int = 0
        self.robots : npt.ArrayLike= np.zeros(16,dtype=object)
        self.add_robots(team_robots)
    
    def __len__(self):
        return self.num_robots
    
    def __getitem__(self,key) -> Robot :
        if isinstance(key,int) and key in range(16): 
            return self.robots[key]
            ## this allows Team[robot_id] -> get robot
    
    def add_robots(self,team_robots:list):
        self.num_robots = len(team_robots)
        for this_robot in team_robots:
            this_id = int(this_robot.robot_id)
            self.robots[this_id] = Robot(isYellow=self.isYellow,robot_data=this_robot)
        
    
        
    def __repr__(self):
        return f"{self.isYellow=} : "