from TeamControl.SSL.vision.frame import FrameList
from TeamControl.network.visionSockets import Vision,VisionTracker
from TeamControl.network.grSimSockets import grSimVision
import numpy as np
import numpy.typing as npt

### THIS IS an example ###

class VisionManager():
    GRSIM_CAMERAS = 4
    REAL_CAMERAS = 1
    VISION = Vision
    GRSIM_VISION = grSimVision
    
    def __init__(self,use_grSim:bool=False):
        self.use_grSim = use_grSim
        self.__set_recv()
        self.field = None
        self.history = 5
        self.frames = FrameList(cameras=self.cameras,history=self.history)

    @property
    def cameras(self):
        return self.GRSIM_CAMERAS if self.use_grSim else self.REAL_CAMERAS
    
    @property
    def has_field(self):
        return self.field is not None
    
    def __set_recv(self):
        self.recv = self.GRSIM_VISION() if self.use_grSim else self.VISION()
    
    def update_detection(self,cycles:int=50) -> bool:
        ## initiate update detection process
        if not isinstance(cycles,int):
            raise TypeError("cycles need to be an integer")
        for _ in range(cycles):
            new_detection_data = self.recv.listen()
            if new_detection_data is not None:
                self.frames.update(new_detection_data)
            if self.frames.is_complete:
                return True
        
        raise TimeoutError("Wrong settings ? ")
    

if __name__ == "__main__" :
    vision = VisionManager()
    print(vision.frames.is_complete)