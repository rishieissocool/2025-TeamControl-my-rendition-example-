from TeamControl.SSL.vision.frame import Frame
from TeamControl.SSL.vision.field import GeometryData
from TeamControl.network.visionSockets import Vision,VisionTracker
import numpy as np
import numpy.typing as npt
from multiprocessing import Queue, Process

### THIS IS a single process ###

class VisionProcess():
    
    def __init__(self,output_q:Queue,use_grSim:bool=True):
        self.use_grSim = use_grSim
        self.output_q = output_q
        self.recv = Vision(port=10006)    
        self.field = None
        self.frame_number = 0
        self.get_update()
    
    @property
    def cameras(self):
        return 4 if self.use_grSim else 1
    
    @property
    def has_field(self):
        return self.field is not None
    

    def get_update(self) -> bool:
        while True:
            new_vision_data = self.recv.listen()
            if new_vision_data.HasField("detection"):
                new_detection_data = new_vision_data.detection
                if self.frame_number < new_detection_data.frame_number:
                    # generates new frame
                    self.frame = Frame.from_proto(new_detection_data,self.cameras)
                    self.frame_number = self.frame.frame_number
                if self.frame_number == new_detection_data.frame_number:
                    self.frame.update(new_detection_data)
                    if self.frame.is_completed:
                        self.send(self.frame)
            if new_vision_data.HasField("geometry"):
                geometry = new_vision_data.geometry
                self.field = GeometryData.from_proto(geometry)
                print(self.field)
                self.send(self.field)
                print("geometry has been initialised")
    
    def send(self,data):
        if not self.output_q.full():
            self.output_q.put(data)
        else:
            raise BufferError ("QUEUE IS FULL")

if __name__ == "__main__" :
    def read(input_q):
        while True:
            if not input_q.empty():
                item = input_q.get_nowait()
                # print(type(item))
            
    output_q = Queue()
    vision = Process(target=VisionProcess,args=(output_q,))
    reader = Process(target=read,args=(output_q,))
    
    vision.start()
    reader.start()
    vision.join()
    reader.join()