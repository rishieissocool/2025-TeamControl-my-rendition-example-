""" SENDER
Sender is an Abstract Base Class (ABC) which includes :
    1. UDP              - UDP socket for server.
    2. Broadcast        - UDP broadcast socket for server.
    3. grSimCommand     - grSim UDP socket for sending Actions.
    # 4. grSimReplacement - grSim UDP socket for sending replacement.
    # 5. grSimTeams       - grSim UDP socket for teams control. 

Raises:
    NotImplementedError: if user try to use an empty function
"""
import socket
import time
import ast

import logging

from TeamControl.shared.Action import Action
from TeamControl.SSL.grSimAction import grSim_Action
from TeamControl.shared.RobotUDP import Sender,UDP
from TeamControl.Network.Robot import Robot

class robotSender(Sender):
    def __init__(self, ip: str = None, port: int = 0) -> None:
        
        super().__init__( ip, port)
        
  
    def send_action(self,action:Action,destination:tuple[str,int]) -> None:
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
        if not isinstance(action,Action):
            raise TypeError("Only Action or byte objects allowed")
        if isinstance(destination,str):
            destination = ast.literal_eval(destination)
        encoded_action:bytes = action.encode()
                # sends the action to destined address
        self.send(msg=encoded_action,destination=destination)
        logging.info(f"SENT : {action=} TO: {destination}")


class grSimSender(Sender):
    def __init__(self, ip: str = "127.0.0.1", port : int = 20010) -> None:
        self.addr = (ip,port)
        super().__init__(ip, port)
    
    def create(self):
        self.sock = self.init_sock(UDP.SOCK_UDP)

    def send(self, message: str, d_addr: tuple[str, int]) -> None:
        raise NotImplementedError("Nothing is here")
    
    def send_action(self, isYellow, action: grSim_Action|bytes) -> None:
        if isinstance(action,grSim_Action):
            action = action.encode()
        if isinstance(action,Action):
           new_action =grSim_Action(isYellow=isYellow,robot_id=action.robot_id,vx=action.vx,vy=action.vy,w=action.w,kick=action.kick,dribble=action.dribble)
           action = new_action.encode()
        # sends packet to grsim
        self.sock.sendto(action,self.addr)


class Broadcast(Sender):
    def __init__(self,port: int = 12342) -> None:
        """
        UDP Broadcast sending channel

        Args:
            port (int, optional): Broadcast channel. Defaults to 12342. *This has to be calibrated with recepients
        
        Params:
            ip (str) : Default broadcast. See python udp_broadcast for more information.
        """
        ip = '<broadcast>'

        # ip = '10.0.0.0'
        self.destination = (ip, port)
        self.sock = self.init_sock(UDP.SOCK_BROADCAST_UDP)
        
def grSimSenderExample():
    main_udp = grSimSender()
    while True: 
        packet = grSim_Action(isYellow=True,robot_id=1,vx=1,vy=2,w=1)
        main_udp.send_action(packet)
        logging.debug(f"Action :  is sent")


if __name__ == "__main__":
    grSimSenderExample()