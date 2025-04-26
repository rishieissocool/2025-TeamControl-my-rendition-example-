
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

from TeamControl.Network.robotCommand import RobotCommand
from TeamControl.Network.baseUDP import BaseSocket,UDP
import yaml
try:
    from yaml import CLoader as Loader
except ImportError as e:
    from yaml import Loader

import socket
import numpy
          
class YamlSender(BaseSocket):
    def __init__(self):
        file = open("src/TeamControl/utils/ipconfig.yaml", "r")
        self.robot = yaml.load(file, Loader)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super().__init__()

        
    
    def send_command(self, command_list:RobotCommand):
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

        for command in command_list:
            robot_id = str(command.robot_id)
            destination = self.robot[robot_id]["ip"]
            port = self.robot[robot_id]["port"]
            print(robot_id,destination,port, command)
            enocded_command:bytes = command.encode()
            self.sock.sendto(enocded_command, (destination, port))
            

if __name__ == "__main__" :
    s = YamlSender()
    list_cmd = [RobotCommand(1),RobotCommand(2),RobotCommand(3),RobotCommand(4)]
    s.send_command(list_cmd)