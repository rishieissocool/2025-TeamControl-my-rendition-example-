""" Processing.py 
Contributors : Emma,  
This file contains how we process the Game Controller data after parsing in Message.py 
This file is an extension of Message.py, in which compares and stores static versions of the data

working in progress
"""

from TeamControl.GameControl.Message import *
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

class Processing():
    def __init__(self,us_yellow: bool=None,us_positive: bool=None):
        self.command:Command = None
        self.us_yellow:bool = us_yellow
        self.us_positive:bool = us_positive
    
    def update(self,ref_msg:RefereeMessage):
        """update
        updates this processing class data
        """
        self._set_command
        self._set_team(ref_msg.blue,ref_msg.yellow, ref_msg.blue_team_on_positive_half)

    def _set_command(self,cmd):
        if self.command != cmd:
            log.info(f"Command has been updated from : {self.command} to : {cmd}")
            self.command = cmd
        if self.command.name == Command.HALT:
            ... 
            
            

    def _set_team(self, blue:TeamInfo, yellow:TeamInfo, blue_is_positive:bool):
        if blue.name == "TurtleRabbit" and self.us_yellow is True:
            # updates us_yellow to false
            self.us_yellow = False
            # self.team_info = blue
        elif yellow.name == "TurtleRabbit" and self.us_yellow is not True:
            self.us_yellow = False
            # self.team_info = yellow
                    
        if blue_is_positive is None:
            return
        elif bool(blue_is_positive) != bool(self.us_yellow):
            self.us_positive = True
        else:
            self.us_positive = False

    
    # def halt(self):
    #     ...
    
    # def stop(self):
    #     ...
        

if __name__ == "__main__":
    from TeamControl.Network.ssl_networking import GameControl
    import time
    
    gc_recv = GameControl()
    gc_processing = Processing()
    
    while True:
        ref_msg = gc_recv.listen()
        start_time = time.time()
        message = RefereeMessage(referee=ref_msg)
        gc_processing.update(message)
        log.debug(f"Internal Processing Time : {time.time() - start_time} \n")
        