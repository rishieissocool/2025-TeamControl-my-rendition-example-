''' World Model - Central Storage and access control
- apply this in multiprocessing or equivalent 
@author - Emma

'''

from TeamControl.SSL.vision.frame_list import FrameList
from TeamControl.SSL.vision.field import GeometryData,FieldSize
from TeamControl.SSL.vision.frame import Frame
from TeamControl.SSL.game_controller.Message import *

from multiprocessing import Queue,Manager
import numpy as np
import numpy.typing as npt

import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class STATE(Enum):
    RUNNING = 0
    HALTED = 1
    STOPPED = 2

class WorldModel:
    """
    World Model aka wm
    Description : 
        ...
        
        
    """
    def __init__(self,update_interval:int=5,history:int=60, use_sim:bool=True):
        mgr = Manager()
        self.us_yellow = True
        self.us_positive = True
        self.count = 0
        self.update_interval:int = update_interval
        self.use_sim:bool = use_sim 
        self.frame_list:FrameList[Frame] = FrameList(history=history)
        self.geometry:GeometryData = None
        self.field:FieldSize = None
        self._version = mgr.Value('i', 0)  # int counter
    
    def update_game_data(self,game_data):
        if isinstance(game_data,Command):
            self.update_state(game_data)
        elif isinstance(game_data,tuple):
            if isinstance(game_data[0],TeamInfo):
                self.ref_data.yellow = game_data[0]
                self.ref_data.blue = game_data[1]
        
    def update_state(self,command):
        print(command) 
        match command:
            case Command.HALT:
                return STATE.HALTED
            case Command.STOP:
                return STATE.STOPPED
            case Command.NORMAL_START | Command.FORCE_START:
                return STATE.RUNNING
            
            case Command.TIMEOUT_BLUE:
                return 
            case Command.TIMEOUT_YELLOW:
                return 
            case Command.BALL_PLACEMENT_BLUE:
                return
            case Command.PREPARE_KICKOFF_BLUE:
                return
            case Command.PREPARE_PENALTY_BLUE:
                return
            
            case Command.DIRECT_FREE_BLUE:
                return
            case Command.INDIRECT_FREE_BLUE:
                return
            
            case Command.BALL_PLACEMENT_YELLOW:
                return
            case Command.PREPARE_KICKOFF_YELLOW:
                return
            case Command.PREPARE_PENALTY_YELLOW:
                return
            
            case Command.DIRECT_FREE_YELLOW:
                return
            case Command.INDIRECT_FREE_YELLOW:
                returnd received: {command}")
            

    def update_team(self,us_yellow:bool,us_positive:bool):
        self.us_yellow = us_yellow
        self.us_positive = us_positive
    
    def add_new_frame(self,frame:Frame):
        self.count += 1
        if self.count >= self.update_interval:
            self._version.value +=1
            self.count = 0
        self.frame_list.append(frame)

    def update_geometry(self,geometry:GeometryData):
        self.geometry = geometry
        self.field = geometry.field
        self.ball_model = geometry.models


    def get_latest_frame(self):
        return self.frame_list.latest
    
    def get_yellow_robots(self,isYellow, robot_id=None):
        if isYellow is True:
            if isinstance(robot_id,int):
                return self.frame_list.latest.robots_yellow[robot_id]
            return self.frame_list.latest.robots_yellow
        elif isYellow is False :
            if isinstance(robot_id,int):
                return self.frame_list.latest.robots_blue[robot_id]
            return self.frame_list.latest.robots_blue
    
    def get_last_n_frames(self,n:int):
        return self.frame_list.get_last_n_frames(n)
    
    
    def get_version(self):
        return self._version.value
    
# if __name__ == "__main__":
#     import time
