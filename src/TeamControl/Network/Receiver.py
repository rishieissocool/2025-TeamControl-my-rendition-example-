import socket
import logging
import struct
import ast #converting str -> tuple

from google.protobuf import json_format

from TeamControl.Model.world import World as wm
from TeamControl.Model.GameState import State
from TeamControl.Network.BaseUDP import BaseSocket,UDP

from TeamControl.Coms.proto2 import ssl_vision_wrapper_pb2
from TeamControl.Coms.proto2 import ssl_gc_referee_message_pb2

import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class Receiver(BaseSocket):
    def __init__ (self,ip: str=None, port: int=0, sock_type=UDP.SOCK_UDP, buffer_size: int=1024):
        """Receiver - init
        Initialising socket for receiving messages

        Args:
            ip (str, optional): ip of device generating receiver. Defaults to None. -> obtaining system ip
            port (int, optional): prefered port number. Defaults to 0 -> auto-generated. 
            sock_type (str, optional): type of socket. Defaults to 'u' - normal UDP socket | alternative  'b' - Broadcast, see init_sock()
            buffer_size (int, optional): size for packet to be received. Defaults to 1024.
        
        Params:
            source(tuple[str,int]) : default sender's address. Currently Not implemented.
                * this should be implemented if we want to only listen from one device (or address)
        """
        super().__init__(ip=ip, port=port, sock_type=sock_type, buffer_size=buffer_size, binding=True)
        print(self)
        
       
    def listen(self, duration: int = None) -> str | None:
        return super().listen(duration)

    
    def _decode(self, data: bytes) -> str | bytes:
        return super()._decode(data)
        
    
    # getting address of this receiver 
    def get_addr(self)->str:
        """ Get Address (Callable function)
        Get the Receiver socket's address

        Returns:
            str: address tuple in the format of string
        """
        addr:tuple = (self.ip,self.port)
        return f"{addr}"
    
    def update_source(self,addr:str|tuple[str,int]):
        """
        Stores source (server or robot) sender address
        Use for verification. 

        Args:
            addr (tuple[str,int]): _description_
        """
        if isinstance(addr, str):
            addr = ast.literal_eval(addr)
        self.recv_addr = addr

    def __repr__(self) -> str:
        msg = f"Reciever: {self.__class__.__name__} created on port: {self.port}, available = {self.ready}"
        return msg

    def send(**kwargs):
        raise NotImplementedError("Please use a sending socket")

class Broadcast_r(Receiver):
    """reciever for broadcast"""
    def __init__(self, port: int = 0, buffer_size: int = 1024):
        sock_type=UDP.SOCK_BROADCAST_UDP
        ip = '<broadcast>'
        super().__init__(ip=ip,port=port,sock_type=sock_type,buffer_size=buffer_size)
        
    

# Multicast Receiver
class Multicast(Receiver):
    def __init__(self,port: int,group:str,decoder:object, buffer_size: int = 6000) -> None:
        """
        Initialising Multicast socket

        Args:
            decoder (object): SSL Protobuf file and descriptor to decode data
            ip (str, optional): ip of Device trying to connect. Defaults to None -> self obtain device ip.
                                if wanted to connect externally, please type in ip string 
            port (int, optional): port of connection. Defaults to 0 -> auto generated.
            group (str, optional): Mulitcast group. Defaults to "224.5.0.0" -> nothing.

        Raises:
            Exception: Needed decoder
        """
        super().__init__(ip="",port=port,sock_type=UDP.SOCK_MULTICAST_UDP,buffer_size=buffer_size)
        
        if decoder is None:
            log.error("No Protobuf Decoder Provided")
            raise Exception("Need Protobuf decoder")
        
        self.group : str = group
        self.decoder:object = decoder
        if self.ready:
            self.ready = self._add_group()
        print(self)
    
    def _add_group(self)-> None:
        """adds group to multicast socket"""
        mreq = struct.pack("=4sl", socket.inet_aton(self.group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return True
        
    def listen(self, duration: int = None) -> bool: # modified to have decoded data to be boolean
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size)
        return super().listen(duration)
    
    def _decode(self,data:bytes) -> bool:
        """
        Reading and decoding the data (overrides super)

        Args:
            data (bytes): data received from listen ()

        Returns:
            str: decoded data
        """
        # Decode with Protobuf 
        # try:
        decoded_data:str= self.decoder.FromString(data) 
        return decoded_data
    
   
