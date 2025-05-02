import numpy as np
import numpy.typing as npt

from TeamControl.SSL.vision.field import *
from TeamControl.world.vision_worker import VisionWorker
from TeamControl.SSL.game_control.Processing import Processing

from multiprocessing import Queue,Process

import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class WorldModel:
    """
    World Model aka wm
    Description : 
        ...
        
        
    """
    def __init__(self, us_yellow : bool=None, us_positive : bool=None, history:int=5, use_sim: bool = False):
        self.use_sim = use_sim 
        self.us_yellow : bool= us_yellow
        self.us_positive : bool= us_positive
        self.history:int = history # histroy length
        self.vision_q = Queue()
        self.gc_q = Queue()
        
        self.vision_wkr = Process(target=VisionWorker, args=(True,self.vision_q,use_sim,history,))
        # self.gc_wkr = Processing(output=self.gc_q)
        # self.field_manager = Field_manager
        self.p2 = Process(target=WorldModel.internal_process)
        self.start()
    
    def start(self):
        self.vision_wkr.start()
        self.p2.start()
        
        self.p2.join()
        self.vision_wkr.join()
    @property
    def detection(self):
        return self.vision_wkr.frames
    @staticmethod
    def internal_process():
        while True:
            for i in range(100):
                print(i)

if __name__ == "__main__":
    import time
    wm = WorldModel(use_sim=True,history=60)
