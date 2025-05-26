''' World Model - Central Storage and access control
- apply this in multiprocessing or equivalent 
@author - Emma

'''

from TeamControl.SSL.vision.frame_list import FrameList
from TeamControl.SSL.vision.field import GeometryData,FieldSize
from TeamControl.SSL.vision.frame import Frame

from multiprocessing import Queue,Manager
import numpy as np
import numpy.typing as npt

import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class WorldModel:
    """
    World Model aka wm
    Description : 
        ...
        
        
    """
    def __init__(self,update_interval:int=5,history:int=60, use_sim:bool=True):
        mgr = Manager()
        self.count = 0
        self.update_interval:int = update_interval
        self.use_sim:bool = use_sim 
        self.frame_list:FrameList[Frame] = FrameList(use_sim,history=history)
        self.geometry:GeometryData = None
        self.field:FieldSize = None
        self._version = mgr.Value('i', 0)  # int counter
    
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
    
    
    def get_version(self):
        return self._version.value
    
# if __name__ == "__main__":
#     import time
