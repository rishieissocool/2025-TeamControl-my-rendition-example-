
import numpy as np

class Ball:
    def __init__(self,ball_data)->object:
        self.c = float(ball_data.confidence)
        self.x = float(ball_data.x).__round__(4)
        self.y = float(ball_data.y).__round__(4)
        self.px = float(ball_data.pixel_x).__round__(4)
        self.py = float(ball_data.pixel_y).__round__(4)
    
    
    def __repr__(self):
        return f"BALL \n Confidence : {self.c:.4f}\n POSITION : {self.position} \n PIXEL : {self.px:.4f}, {self.py:.4f}\n"
        
    @property
    def position (self):
        return np.array([self.x,self.y],dtype=np.float32)
    

