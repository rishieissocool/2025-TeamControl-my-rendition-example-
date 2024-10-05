import socket
import logging
import struct
from google.protobuf import json_format

from TeamControl.Model.world import World as wm
from TeamControl.Model.GameState import State
from TeamControl.shared.RobotUDP import Receiver,UDP

from TeamControl.Coms.proto2 import ssl_vision_wrapper_pb2
from TeamControl.Coms.proto2 import ssl_gc_referee_message_pb2

import logging
log = logging.getLogger()
log.setLevel(logging.NOTSET)


class robotReceiver(Receiver):
    """ Server Robot Receiver
    Subclass of Receiver in Robot UDP, see in shared.RobotUDP

    Args:
        Receiver (Receiver): a Class within RobotUDP file under shared
    """
    def __init__ (self,ip: str=None, port: int=0, sock_type=UDP.SOCK_UDP,buffer_size: int=1024) -> None:
        super().__init__(ip, port,sock_type,buffer_size)
    

# Multicast Receiver
class Multicast(Receiver):
    """ Multicast Receiver
    Subclass of Receiver in Robot UDP, see in shared.RobotUDP

    Args:
        Receiver (Receiver): a Class within RobotUDP file under shared
    """
    def __init__(self,port: int,group:str,decoder:object, ip: str = None) -> None:
        """
        Initialising Multicast socket

        Args:
            model (wm|State): current World Model or State model
            decoder (object): SSL Protobuf file and descriptor to decode data
            ip (str, optional): ip of Device trying to connect. Defaults to None -> self obtain device ip.
                                if wanted to connect externally, please type in ip string 
            port (int, optional): port of connection. Defaults to 0 -> auto generated.
            group (str, optional): Mulitcast group. Defaults to "224.5.0.0" -> nothing.

        Raises:
            ValueError: Wrong model input, please check again
            Exception: Needed decoder
        """
        
        if ip is None: 
            self.ip:str = self.obtain_sys_ip() #gets local ip
        else:
            self.ip:str = ip #use provided ip
        if decoder is None:
            raise Exception("Need Protobuf decoder")
        
        self.port : int = port
        self.group : str = group
        self.buffer_size : int = 6000
        self.decoder:object = decoder
        self.ready = self.create_sock()
        print(self)
    
    def create_sock(self)-> None:
        """Create Socket
            Creates socket to Listen to Multicast
        """
        # set up recieve socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.sock.bind(("", self.port))
        
        mreq = struct.pack("=4sl", socket.inet_aton(self.group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return True
        
    def listen(self, duration: int = None) -> bool: # modified to have decoded data to be boolean
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size)
        return super().listen(duration)
    
    def decode(self,data:bytes) -> bool:
        """
        Reading and decoding the data

        Args:
            data (bytes): data received from listen ()

        Returns:
            str: decoded data
        """
        # Decode with Protobuf 
        # try:
        decoded_data:str= self.decoder.FromString(data) 
        return decoded_data
    
    def __repr__(self) -> str:
        msg = f"Multicast: {self.__class__.__name__} created on port: {self.port}, available = {self.ready}"
        return msg

# Classes of SSL Receivers

class GameControl(Multicast):
    
    def __init__ (self,ip : str=None, port : int=10003)-> None:
        """
        Initialising Multicast Vision SSL Socket

        Args:
            world_model (wm): current world model
            ip (str, optional): ip of Device. Defaults to None -> local. input if other device
            port (int, optional): Port for Game Controller Referee. Defaults to 10003. consult if changing
        """
        decoder :object = ssl_gc_referee_message_pb2.Referee()
        group : str = "224.5.23.1"
        # group : str = "GC.GlOBAL"
        super().__init__(port, group, decoder, ip)

    def listen(self, duration: int = None) -> State:
        state_data = super().listen(duration)
        state = json_format.MessageToDict(state_data)
        # logging.info("{TIME}:states recved")
        # print(type(state_data),type(state))
        new_state = State(**state)
        return new_state

   
# Classes of Vision Wolrd Receivers
class vision(Multicast):
    """ Vision SSL multicast receiver
        world vision SSL  mulitcast listener
    Args:
        Multicast (Class): base Class
    """
    def __init__(self, world_model: wm, ip : str=None, port : int=10005) -> None:
        """
        Initialising Multicast Vision SSL Socket

        Args:
            world_model (wm): current world model
            ip (str, optional): ip of Device. Defaults to None -> local. input if other device
            port (int, optional): Port for Vision World multicast. Defaults to 10005. change accordingly if needed
        """
        if not isinstance(world_model, wm) :
            raise ValueError('Wrong world_model input, *world_model has to be a Model object from TeamControl.World.model.')
        decoder :object = ssl_vision_wrapper_pb2.SSL_WrapperPacket()
        group : str = "224.5.23.2"
        # group = "VISIONSSL.GLOBAL"
        super().__init__(port, group, decoder, ip)
        self.world_model = world_model
   
    def listen(self, duration: int = None) -> bool:
        new_data = super().listen(duration)
        # log.info(new_data)
        is_updated:bool = self.world_model.update(new_data)
        # logging.info()
        return is_updated
    
    
class grSimVision(vision):
    """ grSim Vision multicast receiver
        grSim - vision world mulitcast
    Args:
        Multicast (Class): base Class
    """
    def __init__(self, world_model: wm, ip : str=None, port : int=10020) -> None:
        """
        Initialising Multicast GR Sim World Socket
        
        Args:
            ip (str, optional): ip of the grSim device. Defaults to None -> local.
            port (int, optional): port of grSim Vision. Defaults to 10020.
        """
        super().__init__(world_model,ip,port)
        
class grSimControl(Receiver):
    def __init__(self, ip: str = None, port: int = 10300) -> None:
        """Initiate grSim Control sender and receiver.

        Args:
            ip (str, optional): Ip of Simulation Device. Defaults to None -> self obtain.
            port (int, optional): _description_. Defaults to 10300.
        """
        super().__init__(ip, port)
    
    def listen(self, duration: int = None) -> str:
        return super().listen(duration) 

    def decode(self,data):
        decoded_data:str = self.decoder.FromString(data)
        print("data received : ", decoded_data)
        return decoded_data

    def send (self,packet) -> None:
        self.sock.sendto(packet,(self.ip,self.port))
        ...
    
class grSimYellowControl(grSimControl): 
    def __init__(self, ip: str = None, port: int = 10301) -> None:
        super().__init__(ip, port)
    
    def listen(self, duration: int = None) -> str | None:
        return super().listen(duration)

    def send(self, packet) -> None:
        return super().send(packet)

class grSimBlueControl(grSimControl):
    def __init__(self, ip: str = None, port: int = 10302) -> None:
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
        
if __name__ == "__main__":
    # testing gamae controller receiver
    updated = False
    world_model = wm()
    receiver:Multicast = grSimVision(world_model)
    while True:
        receiver.listen()
            