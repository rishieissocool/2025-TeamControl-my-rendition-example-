
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
    def __init__(self,send_to_grSim:bool):
        path = Path(__file__).resolve()
        # print(path)

        file = open(path.parent / "ipconfig.yaml", "r")
        self.set_robot_addr(yaml.load(file, Loader))
        self.send_to_grSim = send_to_grSim
        super().__init__(type=SocketType.SOCK_UDP,ip='')

    def set_robot_addr(self,raw):
        self.blue = {
            v["shellID"]: {
                "addr": (v["ip"], v["port"]),
                "raw": r
            }
            for r, v in raw["blue"].items()
        }
        
        self.yellow = {
                
            v["shellID"]: {
                "addr": (v["ip"], v["port"]),
                "raw": r
            }
            for r, v in raw["blue"].items()
        }
        print(self.blue)
        self.grSim = (raw["grSim"]["ip"], raw["grSim"]["port"])
    
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
        destination:tuple = self.yellow[robot_id]["addr"] if isYellow is True else self.blue[robot_id]["addr"]
        enocded_command:bytes = command.encode()
        self.sock.sendto(enocded_command, destination)
        print(robot_id,isYellow,destination, command, " Message Sent")
        if self.send_to_grSim is True:
            self.send_grSim_command(command=command)

    def send_grSim_command(self,command:RobotCommand):
        isYellow = command.isYellow
        robot_id = command.robot_id

        raw_robotID = self.yellow[robot_id]["raw"] if isYellow is True else self.blue[robot_id]["raw"]
        if raw_robotID != command.robot_id:
            print("robotID is different, updating command robot ID ")
            command.robot_id = raw_robotID
        enocded_command = command.encode_grSim()
        destination = self.grSim
        self.sock.sendto(enocded_command, destination)
        print(command,destination, " Message Sent to grSim")

        
            
if __name__ == "__main__" :
    s = YamlSender(send_to_grSim=True)
    command = RobotCommand(1)
    s.send_command(command)
    # grSim command 
    # s.send_grSim_command(command)