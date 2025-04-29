from TeamControl.SSL.vision.robots import Team,Robot
from TeamControl.SSL.vision.balls import Ball
from collections import deque

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
    """
    This class contains the FrameDetection Protobuf Data
    It has the following attributes:
    
    frame_number (int) : this number of frame
    balls (list[Ball]) : a list of balls currently on the field
    robots_yellow (Team) : the Team of robots with team color : yellow
    robots_blue (Team) : the Team of robots with team color : blue
    
    Additional Attribute : 
        ball (Ball) : gets the first available ball out of self.balls
    """
    def __init__(self,frame_number:int, balls: list[Ball],robots_yellow:Team, robots_blue:Team, cameras:int=4) -> object:
        self._balls: list[Ball]= [] #init
        self.fully_initialized:bool=False
        self.cameras:int = cameras

        self.frame_number: int= frame_number
        self.balls= balls
        self.robots_yellow: Team= robots_yellow
        self.robots_blue: Team= robots_blue
    
    @property
    def ball(self) -> Ball: 
        # returns the first ball
        return self._balls[0] if self._balls else None
    
    @property
    def balls(self) -> list:
        return self._balls
    
    @balls.setter
    def balls(self,balls_in_frame):
        for data in balls_in_frame:
            new_ball = Ball(data)
            self._balls.append(new_ball)
        
    def __repr__(self) -> str:
        return f"{self.frame_number=},\n {self.balls=}, {self.robots_yellow=}\n {self.robots_blue=}"
        
    @classmethod
    def from_proto(cls,frame_data):
        return cls(
            frame_number=frame_data.frame_number,
            balls=frame_data.balls,
            robots_yellow=Team(frame_data.robots_yellow),
            robots_blue=Team(frame_data.robots_blue)
        )
    
    def update(self,new_frame_data):
        self._balls += new_frame_data.balls
        self.robots_blue += new_frame_data.robots_blue
        self.robots_yellow += new_frame_data.robots_yellow
        
        if new_frame_data.camera_id == self.cameras -1:
            self.fully_initialized = True
       
class FrameList ():
    ### THIS IS A LIST CLASS so this would work like a list
    def __init__(self,frame,cameras:int=1,history:int=5):
        self.newest_frame = 0
        self.cameras = cameras
        self.history = history
        self._frames = deque(frame if frame is not None else [], maxlen=history)
    
    def __getitem__(self, index):
        return self._frames[index]

    def __setitem__(self, index, value):
        self._frames[index] = value

    def __len__(self):
        return len(self._frames)

    def __iter__(self):
        return iter(self._frames)

    def append(self, value):
        self._frames.append(value)

    def update(self, new_detection):
        if new_detection.frame_number == self.newest_frame:
            self.get_latest().update(new_detection)
        elif new_detection.frame_number > self.newest_frame:
            self.newest_frame = new_detection.frame_number
            frame = Frame(new_detection)
            self.append(frame)

    def get_latest(self):
        return self._frames[-1] if self._frames else None

    def clear(self):
        self._frames.clear()
    
    def __repr__(self):
        return repr(self._frames)