from TeamControl.SSL.vision.Process import VisionProcess
from TeamControl.world.worker import BaseWorker
from multiprocessing import Queue
class VisionWorker(BaseWorker):
    def __init__(self, run,output: Queue, use_grSim=False, history=5):
        self.vision = VisionProcess(use_grSim=use_grSim, history=history)
        super().__init__(run, output)


    def step(self):
        while self.running is True:
            self.vision.update_detection()
            self.send(self.vision.frames)
    
