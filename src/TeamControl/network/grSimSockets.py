# from TeamControl.SSL.proto2 import grSim_Commands_pb2,grSim_Packet_pb2
# from TeamControl.SSL.proto2 import grSim_Replacement_pb2,ssl_simulation_control_pb2,ssl_simulation_robot_feedback_pb2,ssl_simulation_robot_control_pb2

from TeamControl.network.sender import Sender
from TeamControl.network.receiver import Receiver
from TeamControl.network.robotCommand import RobotCommand
from TeamControl.SSL.grSim.commands import GrSimRobotCommands

from TeamControl.network.visionSockets import Vision 

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
    def __init__(self,isYellow:bool, ip: str = "127.0.0.1", port : int = 20010) -> None: #please check and verify this port
        # self.destination = (ip,port)
        self.GSC = GrSimRobotCommands(isYellow=isYellow)
        super().__init__(ip=ip,port=port)

    def send(self, command: object) -> None:
        """send_command
        command (bytes) : bytestring serialised by 
        """
        if isinstance(command,RobotCommand):
            self.GSC.convert(command)
        try :
            command = self.GSC.pack(command)
        except Exception as e:
            raise Exception("Error encountered in packing : ", e)
        
        self.sock.sendto(command,self.destination)



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
  
