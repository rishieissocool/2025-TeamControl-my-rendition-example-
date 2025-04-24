"""This is the file for all ssl sockets

Raises:
    ValueError: cannot be decoded
"""
from TeamControl.Network.Receiver import *
from TeamControl.Network.Sender import *

### GC - Recv
class GameControl(Multicast):
    def __init__ (self, port : int=10003)-> None:
        """
        Initialising Multicast Vision SSL Socket

        Args:
            world_model (wm): current world model
            ip (str, optional): ip of Device. Defaults to None -> local. input if other device
            port (int, optional): Port for Game Controller Referee. Defaults to 10003. consult if changing
        """
        decoder :object = ssl_gc_referee_message_pb2.Referee()
        group : str = "224.5.23.1"
        buffer_size : int = 6000
        # group : str = "GC.GlOBAL"
        super().__init__(port=port, group=group, decoder=decoder,buffer_size=buffer_size)

    def listen(self, duration: int = None) :
        ref_msg = super().listen(duration)
        return ref_msg



   
# Classes of Vision Wolrd Receivers
class vision(Multicast):
    """ Vision SSL multicast receiver
        world vision SSL  mulitcast listener
    Args:
        Multicast (Class): base Class
    """
    def __init__(self, world_model: wm, port : int=10005) -> None:
        """
        Initialising Multicast Vision SSL Socket

        Args:
            world_model (wm): current world model
            port (int, optional): Port for Vision World multicast. Defaults to 10005. change accordingly if needed
        """
        if not isinstance(world_model, wm) :
            raise ValueError('Wrong world_model input, *world_model has to be a Model object from TeamControl.World.model.')
        decoder :object = ssl_vision_wrapper_pb2.SSL_WrapperPacket()
        group : str = "224.5.23.2"
        buffer_size : int = 6000
        # group = "VISIONSSL.GLOBAL"
        super().__init__(port=port,group=group,decoder=decoder,buffer_size=buffer_size)
        self.world_model = world_model
   
    def listen(self, duration: int = None) -> bool:
        new_data = super().listen(duration)
        is_updated:bool = self.world_model.update(new_data)
        log.info(f"World Model has been updated")
        return is_updated
    
    
class grSimVision(vision):
    """ grSim Vision multicast receiver
        grSim - vision world mulitcast
    Args:
        Multicast (Class): base Class
    """
    def __init__(self, world_model: wm, port : int=10020) -> None:
        """
        Initialising Multicast GR Sim World Socket
        
        Args:
            ip (str, optional): ip of the grSim device. Defaults to None -> local.
            port (int, optional): port of grSim Vision. Defaults to 10020.
        """
        super().__init__(world_model=world_model,port=port)
        
### Simulation Control ### 

class grSimSender(Sender):
    def __init__(self, ip: str = "127.0.0.1", port : int = 20010) -> None: #please check and verify this port
        self.destination = (ip,port)
        super().__init__(ip=ip,port=port)

    def send(**kwargs) -> None:
        raise NotImplementedError("please use send_command()")
    
    def send_command(self, Command: grSimRobotCommand|RobotCommand, isYellow:bool=None) -> None:
        """send_command
        
        sending Command over grsim command sender port
        
        can parse in either GRSIM Command or RobotCommand message type

        Args:
            isYellow (bool): controlling team is yellow
            Command (grSimRobotCommand|Command|bytes): either a RobotCommand or grSimRobotCommand Message Class
        """
        if isinstance(Command,grSimRobotCommand):
            Command = Command.encode()
        elif isinstance(Command,RobotCommand):
            if isYellow is None:
                raise AttributeError("isYellow is required, please fill in isYellow=True/False")
            new_Command =grSimRobotCommand(isYellow=isYellow,robot_id=Command.robot_id,vx=Command.vx,vy=Command.vy,w=Command.w,kick=Command.kick,dribble=Command.dribble)
            Command = new_Command.encode()
        else:
            return
        # sends packet to grsim
        self.sock.sendto(Command,self.destination)



### NOT IN USE ###
## These are 2 way sockets
class grSimControl(BaseSocket):
    def __init__(self, ip: str = "127.0.0.1", port: int = 10300) -> None:
        """Socket for communicating with grSim Control

        Args:
            ip (str, optional): Ip of Simulation Device. Defaults to None -> self obtain.
            port (int, optional): simulation control port. Defaults to 10300.
        """
        buffer_size = 1024
        self.decoder = None
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
  
