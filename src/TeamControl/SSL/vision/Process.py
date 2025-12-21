from TeamControl.SSL.vision.frame import Frame
from TeamControl.SSL.vision.field import GeometryData
from TeamControl.network.ssl_sockets import Vision,VisionTracker
from TeamControl.utils.Logger import LogSaver

from TeamControl.network.ssl_sockets import Vision,VisionTracker
from TeamControl.utils.Logger import LogSaver

import numpy as np
import numpy.typing as npt
import time
from multiprocessing import Queue, Process



class VisionProcess():
    GRSIM_CAMERAS = 4
    REAL_LIFE_CAMERAS = 1
    
    def __init__(self,is_running,output_q:Queue,logger,use_grSim:bool=True,vision_port=10006):
        self.logger:LogSaver = logger
        self.use_grSim = use_grSim
        self.output_q = output_q
        self.recv = Vision(is_running=is_running,port=vision_port)    
        self.field = None
        self.frame = None
        self.frame_number = -1
        self.logger.info(f"now listening on {vision_port}, using grSim ? {use_grSim} cameras : {self.cameras}")
        self.error_loop_count =0 
        
    @property
    def cameras(self):
        return self.GRSIM_CAMERAS if self.use_grSim is True else self.REAL_LIFE_CAMERAS
    
    @property
    def has_field(self):
        return self.field is not None
    

    def run(self,is_running) -> bool:
        while is_running.is_set():
            new_vision_data = self.recv.listen()
            if new_vision_data is None: 
                # if we want to shut it down after trying ? 
                self.error_loop_count += 1
                if self.error_loop_count > 5:
                    self.logger.error("This is None ? ")
                    self.error_loop_count = 0
                    # exit()
                continue
            
            if new_vision_data.HasField("detection"):
                new_detection_data = new_vision_data.detection
                if self.frame_number < new_detection_data.frame_number:
                    self.logger.info(f"We get new frame : {new_detection_data.frame_number}")
                    # generates new frame
                    self.frame = Frame.from_proto(new_detection_data,self.cameras)
                    self.frame_number = self.frame.frame_number
                
                # if same frame number = it is old frame
                if self.frame_number == new_detection_data.frame_number:
                    # we update the original frame
                    self.frame.update(new_detection_data)
                    if self.frame.is_completed:
                        self.logger.info(f"frame: {self.frame_number} has been completed with {self.cameras} cameras , time taken = {time.time() - loop_timer}")
                        self.send(self.frame)
            if new_vision_data.HasField("geometry"):
                geometry = new_vision_data.geometry
                self.field = GeometryData.from_proto(geometry)
                self.logger.info(f"frame: {self.frame_number} has geometry")
                self.send(self.field)
            loop_timer = time.time()
        
        print("vision_process quit")
    
    def send(self,data):
        if not self.output_q.full():
            self.output_q.put(data)
        else:
            self.logger.warning("QUEUE IS FULL")

def vision_worker(is_running,output_q:Queue,use_grSim:bool=True,vision_port=10006):
    logger = LogSaver()
    v = VisionProcess(is_running,output_q,logger,use_grSim,vision_port)
    logger.info("Initialisation completed, now running . . .")
    v.run(is_running)

if __name__ == "__main__" :
    def read(input_q):
        while True:
            if not input_q.empty():
                item = input_q.get_nowait()
                # print(type(item))
                # print(type(item))
            
    output_q = Queue()
    vision = Process(target=vision_worker,args=(output_q,))
    reader = Process(target=read,args=(output_q,))
    
    vision.start()
    reader.start()
    vision.join()
    reader.join()