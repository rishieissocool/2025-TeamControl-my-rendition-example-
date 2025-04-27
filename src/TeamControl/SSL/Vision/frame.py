from TeamControl.SSL.vision.robots import Team,Robot
from TeamControl.SSL.vision.balls import Ball

import numpy as np
import numpy.typing as npt
import logging

log = logging.getLogger()
log.setLevel(logging.NOTSET)

debug = False

def debug_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)
 
class Frame():
   
    def __init__(self,frame_data) -> object:
        self.frame_number : int = frame_data.frame_number
        self.balls:list = frame_data.balls
        self.robots_yellow:Team = Team(frame_data.robots_yellow)
        self.robots_blue:Team = Team(frame_data.robots_blue)
    
    @property
    def ball(self)->Ball: 
        # returns the first ball
        return self._balls[0] if self._balls else None
    
    @property
    def balls(self) -> list:
        return self._balls
    
    @balls.setter
    def balls(self,balls_in_frame):
        self._balls = [] #init
        for data in balls_in_frame:
            new_ball = Ball(data)
            self._balls.append(new_ball)
        
    
    def __repr__(self) -> str:
        return f"{self.frame_number=},\n {self.balls=}, {self.robots_yellow=}\n {self.robots_blue=}"
        
