# typings
from multiprocessing import Process, Queue, Event
from TeamControl.utils.Logger import LogSaver

class BaseWorker():
    def __init__(self,is_running:Event,logger:LogSaver):
        self.is_running = is_running
        self.logger:LogSaver = logger
        
        
    def step(self):
        """
        each step in the loop
        replace this for a more functional code :) 
        
        """
        self.logger.info("working")
        time.sleep(1)
    
    def run(self):
        while self.is_running.is_set():
            try:
                self.step()
            except KeyboardInterrupt:
                self.logger.warning(f"[{self.__class__.__name__}]: Force Quitting")
                break
            except Exception as e:
                self.logger.error(f"[{self.__class__.__name__}]: Exception encountered:{e} ")
        
        self.shutdown()
    # do shutdown here 
    def shutdown(self):
        self.logger.info(f"[{self.__class__.__name__}]: task complete, shutting down")
        time.sleep(2)
        self.logger.info(f"[{self.__class__.__name__}]: offline")


def run_worker(worker, is_running, logger ):
    """
    the Multiprocessing Process initiator

    Args:
        worker (BaseWorker): Any worker that is a subclass of this
        is_running (Event): The main Event that controls the running state of the system
    """
    w = worker(is_running,logger)
    w.run()

if __name__ == "__main__": 
    import sys
    import time
    logger = LogSaver()
    is_running = Event()
    is_running.set()
    worker = Process(target=run_worker,args=(BaseWorker,is_running,logger,))
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