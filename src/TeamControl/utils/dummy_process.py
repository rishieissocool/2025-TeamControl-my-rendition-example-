from TeamControl.world.model import WorldModel
from multiprocessing import Queue
import time

class DummyReader():
    def __init__(self, wm:WorldModel,input_queue:Queue):
        self.wm:WorldModel = wm
        self.last_version = 0
        self.q = input_queue
        
    def loop(self):
        while True:
            if not self.q.empty():
                item = self.q.get_nowait()
                print(item)
            if self.last_version != self.wm.get_version:
                print(f"new version : {self.wm.get_version}")
            
        
def dummy_reader(wm:WorldModel,input_queue: Queue):
    r = dummy_reader(wm,input_queue)
    r.loop()