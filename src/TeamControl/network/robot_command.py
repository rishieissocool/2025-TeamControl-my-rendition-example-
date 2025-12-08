# Robot Commands
import logging
import datetime
import time
from TeamControl.network.proto2 import grSim_Commands_pb2
from TeamControl.network.proto2 import grSim_Packet_pb2



class RobotCommand():
    def __init__(self, robot_id : int, vx : float=0.0, vy: float=0.0, w : float=0.0, kick : int=0, dribble : int=0, time_origin : float= 0.0, isYellow: bool = True):
        """Robot Command (Previously know as Command)
            Object for initialise commands, encode / decode strings for UDP transportation.
        Args:
            robot_id (int) : wanted Robot ID
            vx (float): wanted velocity for x direction
            vy (float): wanted velocity for y direction
            w (float): wanted angular velocity (radians)
            kick (int): wanted to kick : (0/1)
            dribble (int): wanted to dribble : (0,1)
            time_origin (float): when was this packet first created. Default = 0.0
            
        Params:
            time_set(time.time): time of packet generated
        """
        self.time_set: float = time.time()
        self.isYellow: bool = isYellow
        self.robot_id: int = int(robot_id)
        self.vx: float = float(vx)
        self.vy: float = float(vy)
        self.w: float = float(w)
        self.kick: int = int(kick)
        self.dribble: int = int(dribble)
        self.time_origin: float = float(time_origin)
    
    def __str__(self) -> str:
        return f"{self.robot_id} {self.vx} {self.vy} {self.w} {self.kick} {self.dribble} {self.time_set}"

    def __repr__(self):
        """repr 
            This is a magic function
            It is the representation of Command Class (use for debuging)
        
        return: 
          string : In debuging format of RobotCommand Class objct
        """
        return f'''
    Robot Command: 
    {self.time_set=} , {self.time_origin=} : {self.robot_id=}
    Velocity : {self.vx=} , {self.vy=}, {self.w=}
    Kick? : {self.kick=}
    Dribble? : {self.dribble=}
            '''
        
        
    def encode(self) -> bytes:
        """encode
            Encodes Command object into bytes
            
        Returns:
            bytes: byte data for sending
        
        """
        self.encoded = bytes(str(self).encode('utf-8'))
        return self.encoded
    
    @classmethod
    def decode(cls,command_msg:str|bytes) -> object:
        """decode
            decode and stores the Command to an object *This needs to be a class method
        Args:
            command_msg (str|bytes): message received upon UDP (in the form of string or bytes)
            
        Params: 
            args (arguments): list of arguments to be parsed into creating an RobotCommand Object

        Returns:
            object: RobotCommand object for robot to access
        """
        ## if bytes, decode into string first
        if isinstance(command_msg, bytes):
            command_msg = command_msg.decode()

        robot_id, vx, vy, w, kick, dribble, time_origin = command_msg.split(" ")
        
        args = [int(robot_id), float(vx),float(vy),float(w),int(kick),int(dribble),float(time_origin)]
        
        return RobotCommand(*args) 

    def grSim_robot_command(self) -> object:
        """convert_grSim
            Converts RobotCommand into grSim command protobuff object
        Args:
            isYellow (bool): is the robot yellow ?
        """
        # step 1 : create robot command protobuff object
        grSim_robot_command = self._grSimRobotCommand_wrapper(self.robot_id,self.vx,self.vy,self.w,self.kick,self.dribble)
        # step 2 : create commands protobuff object
        grSim_commands = self._grSimCommand_wrapper(self.isYellow,grSim_robot_command)
        self.grSim_packet = grSim_Packet_pb2.grSim_Packet(commands=grSim_commands)
    
    def grSim_encode(self) -> bytes:
        bytes_packet = self.grSim_packet.SerializeToString()
        return bytes_packet
    
    def _grSimRobotCommand_wrapper(self,robot_id:int,vx: float,vy: float,w: float,k:bool,d:bool) -> object:
        # converts into grSim_Robot_Command (protobuff object)
        kick_speed_x = 10.0
        kick_speed_z = 0.0
        grSim_robot_command =  grSim_Commands_pb2.grSim_Robot_Command(id=robot_id, 
            kickspeedx=(kick_speed_x*k), kickspeedz=(kick_speed_z*k), 
            veltangent=vx, velnormal=vy, velangular=w, 
            spinner=d, wheelsspeed=False)
        return grSim_robot_command
    
    def _grSimCommand_wrapper(self,is_yellow,grSim_robot_command) -> object:
        ## this requires is_yellow input
        # Converts into grSim_Commands (protobuff object)
        grSim_commands = grSim_Commands_pb2.grSim_Commands(timestamp=time.time(),
                                                           isteamyellow=is_yellow,
                                                           robot_commands=[grSim_robot_command])
        return grSim_commands
    