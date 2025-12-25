# typings
from multiprocessing import Queue,Process,Event
from TeamControl.SSL.vision.field import GeometryData
from TeamControl.SSL.vision.frame import Frame
from TeamControl.world.model import WorldModel
from TeamControl.utils.Logger import LogSaver
from TeamControl.ProcessWorkers.worker import BaseWorker
import time


class WMWorker(BaseWorker):
    def __init__(self,is_running,logger):
        self.is_running:Event = is_running
        self.logger = logger
        
    def setup(self, *args):
        wm,vision_q,gc_q = args
        
        self.wm:WorldModel = wm
        self.vision_q:Queue = vision_q
        self.gc_q:Queue = gc_q
        self.delay_time = 0.001 # s
        self.logger.info(f"{self.wm=} \n {self.vision_q=} \n {self.gc_q=} \n {self.delay_time=}")
    
    def step(self):
        if not self.vision_q.empty() :
            item = self.vision_q.get()
            if isinstance(item,Frame):
                self.logger.info("Saving new vision Frame")
                self.wm.add_new_frame(item)
            elif isinstance(item,GeometryData):
                self.logger.info("Updating Geometry")
                self.wm.update_geometry(item)
                        
        if not self.gc_q.empty():
            new_info = self.gc_q.get_nowait()
            self.logger.info(f"Saving new Game Info {new_info}")
            self.wm.update_game_data(new_info)
        
        time.sleep(self.delay_time)
    
    def run(self):
        return super().run()   
    
    def shutdown(self):
        print("[wm_runner] : Going Offline")
        
def run_worker(worker, is_running, logger,*args):
    """
    the Multiprocessing Process initiator

    Args:
        worker (BaseWorker): Any worker that is a subclass of this
        is_running (Event): The main Event that controls the running state of the system
        args(*args) : other optional arguments for setting up 
    """
    w = worker(is_running,logger)
    w.setup(*args)
    w.run()
    
    

if __name__ == "__main__": 
    import sys
    import time
    logger = LogSaver()
    is_running = Event()
    is_running.set()
    wm = WorldModel()
    worker = Process(target=run_worker,args=(WMWorker,is_running,logger,wm,Queue(),Queue(),))
    worker.start()
    for i in range(10):
        try:
            print("[main] : type something to quit")
            s = input()
            print("[main] : finishing this loop")
            is_running.clear()
            break
            
        except KeyboardInterrupt:
            print(f"[main] : Force Quitting workers ")
            is_running.clear()
            sys.exit()

    print("waiting for workers to be shut down")
    worker.join(timeout=4)
    print("All is OFFLINE")