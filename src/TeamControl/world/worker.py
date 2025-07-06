from multiprocessing import Process, Queue
from abc import ABC, abstractmethod

class BaseWorker(Process, ABC):
    def __init__(self, run, output: Queue):
        super().__init__()
        self.running = run
        print(self.running)
        self.output = output
        self.step()

    def send(self, data):
        if not self.output.full():
            self.output.put(data)

    @abstractmethod
    def step(self):
        pass
        
    
    def run(self):
        while True:
            try:
                self.step()
            except Exception as e:
                print(f"[{self.__class__.__name__}] Error: {e}")