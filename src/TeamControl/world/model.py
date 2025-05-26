''' World Model - Central Storage and access control
- apply this in multiprocessing or equivalent 
@author - Emma

'''

from TeamControl.SSL.vision.frame_list import FrameList
from TeamControl.SSL.vision.field import GeometryData
from TeamControl.SSL.vision.frame import Frame

from multiprocessing import Queue,Process
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
    def __init__(self,vision_q:Queue, gc_q:Queue, vision_interval:int, history:int=60, use_sim:bool=True):
        self.use_sim:bool = use_sim 
        self.vision_q:Queue = vision_q
        self.gc_q:Queue = gc_q
        self.interval:int = vision_interval # determines how many frames recv to do an update to all process
        self.frame_list = FrameList(use_sim,history=history)
        self.run()
    
    def run(self):
        count = 0
        while True:
            try:
                if not self.vision_q.empty():
                    item = self.vision_q.get_nowait()
                    if isinstance(item,Frame):
                        self.frame_list.append(item)
                        count += 1
                        if count >= self.interval:
                            self.detection_updated = True
                            print(self.detection_updated)
                            count = 0 
                            self.detection_updated = False
                    elif isinstance(item,GeometryData):
                        self.field = item
                        
                # if not self.gc_q.empty():
                #     new_info = self.gc_q.get_nowait()
                #     self.update_game_data(new_info)
            except Exception as e:
                print("ERROR", e)
    
    # @classmethod
    ## all the method to retrieve data here
    
                
# if __name__ == "__main__":
#     import time
