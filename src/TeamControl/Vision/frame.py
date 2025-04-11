import numpy as np
import numpy.typing as npt
from TeamControl.VoronoiPlanner.Obstacle import Obstacle
import logging

log = logging.getLogger()
log.setLevel(logging.NOTSET)

debug = False

def debug_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)
    
class Robot:
    SELF = 0
    CORDS = 1
    ID = 2
    CONFIDENCE = 3
    PIXEL = 4
    OBS = 5
    XY = 6
    
    def __init__(self,robot_data,isYellow:bool) -> object:
        self.id : int = robot_data.robot_id
        self.isYellow : bool = isYellow
        self.c : float = robot_data.confidence
        self.x : float = robot_data.x
        self.y : float = robot_data.y
        self.o : float = robot_data.orientation
        self.px : float = robot_data.pixel_x
        self.py : float = robot_data.pixel_y
        self.obs : Obstacle = self.__form_obstacles()
    
    # def __lt__(self,other):
    #     return self.id < other.id
    
    def __form_obstacles(self):
        # buffer = 250
        # top_left= [self.x-buffer, self.y+buffer]
        # bottom_right= [self.x+buffer, self.y-buffer]
        # return Obstacle(top_left, bottom_right)
    
        return Obstacle(point=(self.x,self.y),
                        radius=90,
                        unum=self.id,
                        isYellow=self.isYellow)    
    
    
    def get(self,format:int,dp: int= 4)-> object|tuple[float,float,float]|int|float|tuple[float,float]:
        """
        Wildcard function of getting robot attr (*numbers subject to change)
            0.SELF. as object
            1.CORDS. as (x,y,o)
            2.ID. as robot_id [int]
            3.CONFIDENCE as float
            4.PIXEL as pixel_x, pixel_y
            5.OBS. as Obstacles objects for planner

        Args:
            format (int): see above.
            dp (int, optional): decimal place. Defaults to 4.

        Returns:
            object
            |tuple[float,float,float]|int|float|tuple[float,float]: see above.
        """
        match format:
            case self.SELF:
                return self

            case self.CORDS:
                x : float = round(self.x, dp)
                y : float= round(self.y, dp) 
                o : float= round(self.o, dp)
                return x,y,o
            
            case self.ID:
                return self.id
            
            
            case self.CONFIDENCE:
                c : float = round(self.c, dp)
                return c
            
            case self.PIXEL:
                px : float = round(self.px, dp)
                py : float= round(self.py, dp) 
                return px, py
            
            case self.OBS:
                return self.obs
            
            case self.XY:
                x: float = round(self.x, dp)
                y: float = round(self.y, dp) 
                return x,y
            
    def get_position(self) -> tuple[float,float,float]:
        return self.get(format=self.CORDS)
    
    def __repr__(self):
        if self.isYellow is True:
            color = 'Yellow'
        elif self.isYellow is False:
            color = 'Blue'
        return f'''
    
    Team: {color} 
    Robot ID : {self.id} | Confidence : {self.c}
    CORDS: {self.x}, {self.y}, {self.o} | PIXEL : {self.px}, {self.py} 
    OBS : {self.obs} 
    '''
        
        
        

class Ball:
    SELF = 0
    CORDS = 1
    CONFIDENCE = 2
    PIXEL = 3
    def __init__(self,ball_data)->object:
        self.c = ball_data.confidence
        self.x = ball_data.x
        self.y = ball_data.y
        self.px = ball_data.pixel_x
        self.py = ball_data.pixel_y
    
    def get(self, format : int=CORDS, dp : int=4)-> object|tuple[float,float]|float:
        match format:
            case self.SELF:
                return self
            case self.CORDS:
                x: float = round(self.x, dp)
                y: float = round(self.y, dp) 
                return x,y
            case self.CONFIDENCE:
                c: float = round(self.c, dp)
                return c
            case self.PIXEL:
                px: float = round(self.px, dp)
                py: float = round(self.py, dp) 
                return px,py
            
    
    def __repr__(self):
        return f"BALL \n Confidence : {self.c}\n POSITION : {self.x},{self.y} \n PIXEL : {self.px}, {self.py}\n"
        
class Frame():
   
    def __init__(self,frame_data) -> object:
        self.id : int = frame_data.frame_number
        self.yellow_team = None
        self.blue_team = None
        self.ballist = None
        self.update(frame_data)
        # log.info(f"CREATED {self.id}")
         
    def update(self,frame_data):
        balls : list = frame_data.balls
        self.ballist: npt.ArrayLike = self.__extract_balls(balls,self.ballist)
        self.__extract_teams(frame_data)
        # log.info(balls)
        # log.info(self.yellow_team)
        # log.info(self.blue_team)

    
    
    
### EXTRACT ###     
    def __extract_teams(self,frame_data):
        yellow : list = frame_data.robots_yellow
        blue : list = frame_data.robots_blue
        self.yellow_team : npt.ArrayLike = self.__extract_robots(yellow,self.yellow_team,isYellow=True)
        self.blue_team : npt.ArrayLike = self.__extract_robots(blue,self.blue_team,isYellow=False)
        
        #validation check
        assert not self.blue_team is self.yellow_team
    
    @staticmethod
    def __extract_robots(robots : list, robot_arr:npt.ArrayLike,isYellow:bool)-> npt.ArrayLike:
        # if there is no array (new frame)
        if robot_arr is None: 
           robot_arr : npt.ArrayLike = np.zeros(16,dtype=object)
        if len(robots)>0:
            for robot in robots:
                # get robot_id
                robot_id = int(robot.robot_id)
                # initiate new robot object 
                new_robot = Robot(robot,isYellow)
                # append to robotlist
                robot_arr[robot_id]=new_robot
        #sends back array
        return robot_arr
    
    @staticmethod
    def __extract_balls(balls : list, ballist : np.array=None):
        # if No exisitng ballist
        if ballist is None:
            # creates a new ballist
            ballist = np.zeros(10,dtype=object)
        # checks if there are ball data recieved
        if len(balls)>0:
            for i,ball in enumerate(balls):
                # initiate Ball object and adds to ballist
                ballist[i] = Ball(ball)
        else : # No balls here 
            pass
                    
        return ballist

 
    
### GET ### 
    def get_team_robots(self,isYellow: bool,format=None) -> list:
        team_arr = self.__get_team_array(isYellow)
        active_robots: list = list()
        for i in team_arr:
            if isinstance(i,Robot):
                if format is not None:
                    robot_data = i.get(format)
                    active_robots.append(robot_data)
                else: 
                    active_robots.append(i)
        return active_robots
    
        
    def get_robot(self,isYellow:bool,robot_id:int,format=None)-> tuple[float,float,float]|None:
        team_arr = self.__get_team_array(isYellow)

        if robot_id is not None: 
            robot: Robot = team_arr[robot_id]
        else : 
            # return self.get_team_robots(team_arr,format)
            log.error("Please use frame.get_team_robots")
            return None
        
        if isinstance(robot,Robot):
                r: tuple[float,float,float] = robot.get(format)
                # log.info(f"RESULT : {isYellow=} : {robot_id=} : {r=} ")
                return r
        else: 
            log.error(f"No Such robot :{isYellow=}:{robot_id=}")
            return None # No Robot Found

    
    def __get_team_array(self,isYellow:bool)-> npt.ArrayLike:
        if isYellow is True:
            team_arr: npt.ArrayLike = self.yellow_team
        else: 
            team_arr: npt.ArrayLike = self.blue_team
        return team_arr
        
    def get_ball(self,format:int=Ball.CORDS) -> tuple[float,float]|None:
        ball:Ball = self.ballist[0]
        if isinstance(ball,Ball):
            pos = ball.get(format)
            log.info(f"ball is at : {pos=}")
            return pos
        else:
            return None
        
    def has_id(self, isYellow: bool, robot_id: int) -> object:
        if isYellow:
            team = self.yellow_team
        else: 
            team = self.blue_team    
        if isinstance(team[robot_id],Robot):
            return team[robot_id]
        else :
            return None
    
    def __repr__(self) -> str:
        yellow_id = self.get_team_robots(True,format=Robot.ID)
        blue_id = self.get_team_robots(False,format=Robot.ID)
        return f'''
        Frame ID : {self.id}
        
        --- ROBOTS ---
        YELLOW Team: 
        Active: {len(yellow_id)} ID : {yellow_id} 
        Details : 
            {[x for x in self.yellow_team]},\n
        
        BLUE Team: 
        Active: {len(blue_id)} ID : {blue_id} 
        Details : 
            {[x for x in self.blue_team]},\n
        
        --- BALL(s) ---
        Balls: 
            {[x for x in self.ballist]}\n
        '''
        
