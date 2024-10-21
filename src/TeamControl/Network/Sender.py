""" SENDER
Sender includes :
    1. Sender            - UDP socket for server.
    2. Broadcaster       - UDP broadcast socket for server.
    3. Multicaster       - UDP Multicast socket (Not Implemented)
Raises:
    NotImplementedError: if user try to use an empty function
"""
import ast

import logging

from TeamControl.Coms.Action import BaseAction,Action
from TeamControl.Coms.grSimAction import grSim_Action
from TeamControl.Network.BaseUDP import *
# from TeamControl.Network.Robot import Robot

          
class Sender(BaseSocket):
    def __init__(self, ip: str=None, port: int=0, sock_type=UDP.SOCK_UDP, binding=False) -> None:
        if isinstance(ip,str):
            self.destination = (ip,port)
        else:
            self.destination = ("127.0.0.1",port)
        super().__init__(ip=None,port=port,sock_type=sock_type,binding=binding)
    
    def send_action(self,action:BaseAction,destination:tuple[str,int]) -> None:
        """
        Sending Action via UDP

        Args:
            action (Action): Action that wants to be sent
            d_addr (tuple[str,int]): destination address to be delivered to 
            
        Params: 
            encoded_action(bytes): see Action.encode
        Exceptions:
            TypeError : Only Action or byte objects allowed
        """
        # if not isinstance(action,issubclass(BaseAction)):
        #     raise TypeError("Only Actions allowed")
        
        encoded_action:bytes = action.encode()
                # sends the action to destined address
        self.send(msg=encoded_action,destination=destination)
        logging.info(f"SENT : {action=} TO: {destination}")

    def update_destination(self, destination:str|tuple[str,int]) -> None:
        """Update Sending Socket's Destination
        This is a static method, so when the send is trigger, will always send to this specific destination (ip,port)

        Args:
            destination (str | tuple[str,int]): Destination addr, can be in format string / tuple
        """
        if isinstance(destination,str):
            destination = ast.literal_eval(destination)
        self.destination = destination
    
    def listen(self, duration: int = None) -> str | None:
        raise NotImplementedError("Please Use Receiver")


class Broadcaster(Sender):
    def __init__(self,port: int = 12342) -> None:
        """
        UDP Broadcast sending channel

        Args:
            port (int, optional): Broadcast channel. Defaults to 12342. *This has to be calibrated with recepients
        
        Params:
            ip (str) : Default broadcast. See python udp_broadcast for more information.
        """
        ip = '<broadcast>'
        super().__init__(ip=ip,port=port,sock_type=UDP.SOCK_BROADCAST_UDP,binding=True)
        
        
class Multicaster(Sender):
    ...