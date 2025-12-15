# Read YAML file 
import yaml

with open("robots_info.yaml", "r") as f: 
    robot_db = yaml.load(f, Loader = yaml.SafeLoader)

print(robot_db)


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
from .robot_command import RobotCommand
from .baseUDP import BaseSocket,SocketType


          
class YamlSender(BaseSocket):
    def __init__(self):
        self.lookup = robot_db
        super().__init__(type=SocketType.SOCK_UDP,ip='')
    
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
        shell_id = command.robot_id
        destination = self.lookup[shell_id]["ip"]
        port = self.lookup[shell_id]["port"]
        encoded_command:bytes = command.encode()
        self.sock.sendto(encoded_command, (destination, port))
        # print(shell_id,destination,port, command, " Message Sent")


c = RobotCommand(1)
sender = YamlSender()
sender.send_command(c)
