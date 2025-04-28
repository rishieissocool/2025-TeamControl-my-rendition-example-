from TeamControl.SSL.vision.frame import Frame

import numpy as np
import numpy.typing as npt

### THIS IS TEMP ###


class Processing():
    def __init__(self,total_cameras:int=1, history_length:int=5):
        self.current_frame_number:int  = 0 #current frame id
        self.total_cameras:int = total_cameras # max cameras on field
        self.history_length = history_length # history length
        self.frames : list = list()
        self.field = None
        self.is_detection_fully_updated = False

    
    def update(self,protobuf_data):
        if getattr(protobuf_data,"detection"):
            self.update_detection(protobuf_data.detection)
            
        if getattr(protobuf_data,"geometry"):
            self.update_detection(protobuf_data.geometry)
        
    def update_detection(self,protobuf_detection):
        this_frame_number = protobuf_detection.frame_number
        # if the new frame is later than our current latest frame 
        if self.current_frame_number > this_frame_number:
            new_frame = Frame(protobuf_detection)
            self.frames.append(new_frame)
            ## if the length is too long, get rid of the oldest
            if len(self.frames) > self.history_length:
                self.frames.pop(0)
        
        elif self.current_frame_number == this_frame_number:
            # retrieve last frame
            latest_frame = self.frames[-1]
            latest_frame.update(protobuf_detection)
        else :
            print("unexpected result")
            return
        
        # checks if the frame is completed (obtain all field camera data)
        this_camera = protobuf_detection.camera_id
        last_camera_id = self.cameras-1
        if this_camera == last_camera_id: ## this camera is the last camera for the frame
            self.is_detection_fully_updated = True
        else : 
            self.is_detection_fully_updated = False
        
        