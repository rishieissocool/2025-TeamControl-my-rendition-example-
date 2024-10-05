import time
from abc import ABC,abstractmethod

#This is a abstract class

class BaseAction(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def encode(self):
        ...
        
    @abstractmethod
    def decode(self):
        ... 
    
    