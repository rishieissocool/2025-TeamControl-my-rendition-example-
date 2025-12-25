
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

from pathlib import Path
from TeamControl.network.robot_command import RobotCommand
from TeamControl.network.baseUDP import BaseSocket,SocketType
import yaml
try:
    from yaml import CLoader as Loader
except ImportError as e:
    from yaml import Loader


          
class YamlSender(BaseSocket):
    def __init__(self):
        path = Path(__file__).resolve()
        # print(path)

        file = open(path.parent / "ipconfig.yaml", "r")
        self.set_robot_addr(yaml.load(file, Loader))
        super().__init__(type=SocketType.SOCK_UDP,ip='')

    def set_robot_addr(self,raw):
        self.blue = {
                v["shellID"]: (v["ip"], v["port"])
                for _, v in raw["blue"].items()
            }
        
        self.yellow = {
                v["shellID"]: (v["ip"], v["port"])
                for _, v in raw["yellow"].items()
            }
    
    def send_command(self, command:RobotCommand):
        """
        Sending command via UDP

        Args:
            command (RobotCommand): Command that wants to be sent
            d_addr (tuple[str,int]): destination address to be delivered to 
            
        Params: 
            encoded_Command(bytes): see Command.encode
        Exceptions:
            TypeError : Only Command or byte objects allowed
        """
        robot_id = command.robot_id
        isYellow = command.isYellow
        destination:tuple = self.yellow[robot_id] if isYellow is True else self.blue[robot_id]
        enocded_command:bytes = command.encode()
        self.sock.sendto(enocded_command, destination)
        print(robot_id,isYellow,destination, command, " Message Sent")

            
if __name__ == "__main__" :
    s = YamlSender()
    s.send_command(RobotCommand(1))