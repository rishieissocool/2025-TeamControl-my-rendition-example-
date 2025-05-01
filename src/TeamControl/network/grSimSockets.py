# from TeamControl.SSL.proto2 import grSim_Commands_pb2,grSim_Packet_pb2
# from TeamControl.SSL.proto2 import grSim_Replacement_pb2,ssl_simulation_control_pb2,ssl_simulation_robot_feedback_pb2,ssl_simulation_robot_control_pb2

from TeamControl.network.sender import Sender
from TeamControl.network.receiver import Receiver
from TeamControl.network.robotCommand import RobotCommand

from TeamControl.network.visionSockets import Vision 
from TeamControl.network.grSimRobotCommmand import GSRobotCommand

class grSimVision(Vision):
    def __init__(self, port : int=10020) -> None:
        """
        Initialising Multicast GR Sim World Socket
        
        Args:
            ip (str, optional): ip of the grSim device. Defaults to None -> local.
            port (int, optional): port of grSim Vision. Defaults to 10020.
        """
        super().__init__(port=port)
        
### Simulation Control ### 

class grSimSender(Sender):
    def __init__(self, ip: str = "127.0.0.1", port : int = 20010) -> None: #please check and verify this port
        self.destination = (ip,port)
        super().__init__(ip=ip,port=port)

    def send(**kwargs) -> None:
        raise NotImplementedError("please use send_command()")
    
    def send_command(self, Command: GSRobotCommand|RobotCommand, isYellow:bool=None) -> None:
        """send_command
        
        sending Command over grsim command sender port
        
        can parse in either GRSIM Command or RobotCommand message type

        Args:
            isYellow (bool): controlling team is yellow
            Command (grSimRobotCommand|Command|bytes): either a RobotCommand or grSimRobotCommand Message Class
        """
        if isinstance(Command,GSRobotCommand):
            Command = Command.encode()
        elif isinstance(Command,RobotCommand):
            if isYellow is None:
                raise AttributeError("isYellow is required, please fill in isYellow=True/False")
            new_Command =GSRobotCommand(isYellow=isYellow,robot_id=Command.robot_id,vx=Command.vx,vy=Command.vy,w=Command.w,kick=Command.kick,dribble=Command.dribble)
            Command = new_Command.encode()
        else:
            return
        # sends packet to grsim
        self.sock.sendto(Command,self.destination)



### NOT IN USE ###
## These are 2 way sockets
class grSimControl(Sender):
    def __init__(self, ip: str = "127.0.0.1", port: int = 10300) -> None:
        """Socket for communicating with grSim Control

        Args:
            ip (str, optional): Ip of Simulation Device. Defaults to None -> self obtain.
            port (int, optional): simulation control port. Defaults to 10300.
        """
        buffer_size = 1024
        # self.coder = ssl_simulation_control_pb2.
        super().__init__(ip=ip,port=port,buffer_size=buffer_size,binding=False)
    
    def listen(self, duration: int = None) -> str:
        return super().listen(duration) 

    def decode(self,data):
        raise NotImplementedError
        decoded_data:str = self.decoder.FromString(data)
        print("data received : ", decoded_data)
        return decoded_data

    def send (self,packet) -> None:
        self.sock.sendto(packet,(self.ip,self.port))
        ...
    
class grSimYellowControl(grSimControl): 
    def __init__(self, ip: str = "127.0.0.1", port: int = 10301) -> None:
        super().__init__(ip, port)
    
    def listen(self, duration: int = None) -> str | None:
        return super().listen(duration)

    def send(self, packet) -> None:
        return super().send(packet)

class grSimBlueControl(grSimControl):
    def __init__(self, ip: str = "127.0.0.1", port: int = 10302) -> None:
        """grSim Blue Team Control.

        Args:
            ip (str, optional): ip of simulation. Defaults to None.
            port (int, optional): port receiving. Defaults to 10302.
        """
        super().__init__(ip, port)
        
    def listen(self, duration: int = None):
        return super().listen(duration)

    def send(self, packet) -> None:
        return super().send(packet)
  
