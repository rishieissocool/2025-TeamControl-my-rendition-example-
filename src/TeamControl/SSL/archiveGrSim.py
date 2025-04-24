from TeamControl.Coms.proto2 import *
from TeamControl.Model.world import World as wm
from TeamControl.Network.Receiver import *
from TeamControl.Network.Sender import *
from TeamControl.Vision.frame import Robot as r
from TeamControl.RobotBehaviour.goToTarget import *
from TeamControl.Model.transform_cords import *
from sklearn.linear_model import LinearRegression
from TeamControl.Model.world import World as wm
from TeamControl.Coms.grSimRobotCommands import grSimRobotCommand
from TeamControl.Network.ssl_networking import grSimVision, grSimSender
from TeamControl.RobotBehaviour.Movement import *
class grSimServer():
    def __init__(self,isYellow:bool, isPositive:bool, ip:str = None, isPostive = False): 
        self.world_model = wm(isYellow=isYellow, isPositive = isPositive,max_cameras=4)
        self.vision_sock = grSimVision(world_model=self.world_model, ip=ip)
        self.feild_size = (9000,6000)
        self.sender = grSimSender()
        self.isYellow = isYellow
        self.isPostive = isPostive
        self.isPositive = isPositive
    


def run():
    simServer = grSimServer(False, True)
    
            

