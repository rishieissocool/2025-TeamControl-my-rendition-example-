import numpy as np
import numpy.typing as npt

from TeamControl.SSL.vision.frame import Frame, FrameList,Robot,Ball
from TeamControl.SSL.vision.field import *
from TeamControl.SSL.game_control.Message import *
from TeamControl.SSL.proto2 import ssl_gc_referee_message_pb2,ssl_vision_wrapper_pb2


import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class WorldModel:
    """
    World Model aka wm
    Description : 
        This class contains data extracted from Vision world. (Either Simulation or Vision-ssl). 
        
        The model will first compare whether the data is type 'detection' or 'geometry'. 
        
        -- Detection --
        If the data is detection, the model will check the 'Frame Number'.
            if it is an existing one, it will reuse the frame and update new data. 
            if it is a NEW one, it will initiate a new Frame object
            
        -- Geometry --
        if the data is geometry, the model will create an Object of the class : Field
        *since this is a static data, it does not require constant update*
        
    Params : 
        --Booleans--
        usYellow (bool) : is Our Team Yellow
        usPositive (bool) : is Our Team on x-Positive side
        is_detection_updated (bool) : is vision detection updated yet
        has_new_event (bool) : New event from game Controller
        has_new_state (bool) : New state from game controller 
        
        
    """
    def __init__(self, us_yellow : bool=None, us_positive : bool=None, history:int=5, use_sim: bool = False):
        ## basic config 
        self._is_grSim = False


        # vision data
        self.is_detection_fully_updated:bool = False
        self.has_field_geometry:bool = False        
        self.current_frame_number:int  = 0 #current frame id
        self.cameras:int = 1
        self.is_grSim : bool= use_sim

        #static class init
        self.detection_frames = FrameList(cameras=self.max_camera)
        self.field = None

        # game Controller
        self.has_new_state : bool = False
        self.has_new_event : bool= False
        self.current_command : Command= None
        self.current_event : GameEvent= None
        
        # init from args
        self.us_yellow : bool= us_yellow
        self.us_positive : bool= us_positive
        self.history_length:int = history # histroy length
        
    
    @property
    def is_grSim (self):
        return self._is_grSim
    @is_grSim.setter
    def is_grSim(self, use_sim: bool):
        if not isinstance(use_sim,bool):
            raise TypeError ("using_grSim should be a boolean")
        if use_sim is True:
            self.cameras = 4
            self._is_grSim = True 
        else: 
            self.cameras = 1
            self._is_grSim = False
    
    def update(self,proto_data):
        if isinstance(proto_data,ssl_gc_referee_message_pb2.Referee):
            self.update_game(ref_msg=proto_data)
        elif isinstance(proto_data,ssl_vision_wrapper_pb2.SSL_WrapperPacket):
            if proto_data.HasField("detection") :
                self.update_detection(proto_data.detection) 
            if proto_data.HasField("geometry") :
                self.update_geometry(proto_data.geometry)
        
    def update_game(self,ref_msg:ssl_gc_referee_message_pb2):
        new_ref_msg = RefereeMessage(referee=ref_msg)
        if new_ref_msg.command != self.current_command:
            self.has_new_state = True
            self.current_command = new_ref_msg.command
            print(self.current_command)
        
        
    def update_detection (self,detection):
        if detection.frame_number == self.current_frame_number:
            frame = self.frames[-1]
        elif detection.frame_number > self.current_frame_number:
            frame = Frame(frame_data=detection)
            self.frames.append(frame)
            if self.frames > self.history_length:
                self.frames.pop(0)
        
        if detection.camera_id == self.max_camera-1:
            self.is_detection_fully_updated = True
            self.vision_cool_down = time.time()+1    
        
    def update_geometry (self,geometry):
        self.field = GeometryData(geometry)
        self.has_field_geometry = True
        print(geometry)
        
if __name__ == "__main__":
    from TeamControl.network import Vision, grSimVision, GameControl
    import time
    gc_recv = GameControl()
    # vision_recv = grSimVision()
    vision_recv = Vision()
    wm = WorldModel(use_sim=True)
    time_start = time.time()
    # for i in range (100):
    while True:
        if wm.is_detection_fully_updated is False:
            new_vision_data = vision_recv.listen()
            wm.update(proto_data=new_vision_data)
            
        if wm.is_detection_fully_updated is True:
            # print("FULLY UPDATED")
            if wm.vision_cool_down < time.time():
                wm.is_detection_fully_updated = False
            
            
    #         wm.is_detection_fully_updated = False
        new_gc_data = gc_recv.listen()
        wm.update(new_gc_data)
        # print(new_vision_data)
        # print(new_gc_data)