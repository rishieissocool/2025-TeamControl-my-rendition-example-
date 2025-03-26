
"""
This class is going to be replaced. 
"""
import time

from TeamControl.Model.world import World as wm
from TeamControl.Coms.proto2 import grSim_Packet_pb2
from TeamControl.Coms.proto2 import grSim_Commands_pb2
from TeamControl.Coms.proto2 import grSim_Replacement_pb2
# from TeamControl.Coms.proto2 import ssl_vision_wrapper_pb2
# from TeamControl.Coms.proto2 import grSim_Robotstatus_pb2 


TIME = time.time()
### GR SIM ACTION ### 
class grSim_Action():
    """grSim Action
    Class commands to generate action and send to grSim

    Args:
        Packet (grSimPacket): the packet to be sent to grSim
    """ 
    def __init__(self,isYellow:bool, 
                 robot_id:int, 
                 vx=0.0, vy=0.0, w=0.0, 
                 kick=0, dribble=0,
                 ) -> None:
        """initiating Action Object

        Args:
            isYellow (bool): is your team color Yellow?
            robot_id (int): robot ID
            vx (float, optional): velocity in x. Defaults to 0.0.
            vy (float, optional): velocity in y. Defaults to 0.0.
            w (float, optional): angular velocity. Defaults to 0.0.
            kick (int, optional): kick ? [Chip+Normal = 2|Normal = 1|False = 0]. Defaults to False = 0.
            dribble (int, optional): Dribble ? [True = 1|False = 0]. Defaults to False = 0.
        
        Params:
            speed (int) : default kick speed : 10
        """
        speed: int = 5
        self.isYellow  = isYellow
        self.robot_id = int(robot_id)
        self.vx = float(vx)
        self.vy = float(vy)
        self.w = float(w)
        match kick:
            case 0:
                kx,kz = 0,0
            case 1:
                kx, kz = speed,0
            case 2:
                kx, kz = speed,speed
        
        self.kx = float(kx)
        self.kz = float(kz) 
        self.d = bool(dribble)
        
    def encode(self)->bytes:
        cmd = grSim_Action.robot_command(id=self.robot_id,
                                         kickspeedx=self.kx,kickspeedz=self.kz,
                                         veltangent=self.vx, velnormal=self.vy, velangular=self.w,
                                         spinner=self.d)
        commands = grSim_Action.command(isteamyellow=self.isYellow,
                                        robot_commands=[cmd]) 
        action = grSim_Action.packet(commands)
        encoded_action = action.SerializeToString()
        return encoded_action
    
    
    def decode(self):
        raise NotImplementedError
    
    @staticmethod
    def robot_command(id, kickspeedx=0.0, kickspeedz=0.0, veltangent=0.0, velnormal=0.0,
                            velangular=0.0, spinner=False, wheelsspeed=False, wheel1=0.0, wheel2=0.0, 
                            wheel3=0.0, wheel4=0.0):
        
        return grSim_Commands_pb2.grSim_Robot_Command(
            id=id, kickspeedx=kickspeedx, kickspeedz=kickspeedz, veltangent=veltangent, 
            velnormal=velnormal, velangular=velangular, 
            spinner=spinner, wheelsspeed=wheelsspeed, wheel1=wheel1, wheel2=wheel2, 
            wheel3=wheel3, wheel4=wheel4
        )
    @staticmethod
    def command(isteamyellow, robot_commands):
        timestamp = 0.0
        return grSim_Commands_pb2.grSim_Commands(
            timestamp=timestamp, isteamyellow=isteamyellow, robot_commands=robot_commands
        )
   
    @staticmethod
    def packet(commands=None, replacements=None):
        if commands is not None:
            packet = grSim_Packet_pb2.grSim_Packet(commands=commands)
        if replacements is not None:
            packet = grSim_Packet_pb2.grSim_Packet(replacement=replacements)
        elif commands is not None and replacements is not None:
            packet = grSim_Packet_pb2.grSim_Packet(commands=commands,replacement=replacements)
        return packet
    

    def __repr__(self) -> str:
        return f"GRSIM Action : {self.isYellow=}, {self.robot_id}\n Velocities :\n x: {self.vx}, y: {self.vy}, w: {self.w} \n Kicker :\n x: {self.kx}, z :{self.kz}"