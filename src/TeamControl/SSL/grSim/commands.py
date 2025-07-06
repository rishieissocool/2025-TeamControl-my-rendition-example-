# this is to get us ready to turn the commands to grSim RobotCommands
from TeamControl.network.robotCommand import RobotCommand
# from TeamControl.robot.robot_commands import RobotCommands # do not use
# proto import
from TeamControl.SSL.proto2 import grSim_Commands_pb2
from TeamControl.SSL.proto2 import grSim_Packet_pb2

import time

class GrSimRobotCommands:
    def __init__(self,isYellow: bool):
        self.isYellow : bool = isYellow 
        self.kick_speed_x : float = 10.0
        self.kick_speed_z : float = 0.0 #we have no chip kick
        self.wheel_speed : bool = False
        
    def update_is_yellow(self,new_is_Yellow: bool) -> None:
        # at any time if you want to switch 
        self.isYellow = new_is_Yellow
        # log update
    
    def team(self,us:bool) -> bool:
        is_yellow = self.isYellow if us is True else not(self.isYellow)
        return is_yellow
    
    def _robot_command_wrapper(self,robot_id:int,vx: float,vy: float,w: float,k:bool,d:bool) -> object:
        # the follow converts the data types, if you got a problem, check your code
        robot_id = int(robot_id)
        vx = float(vx)
        vy = float(vy)
        w = float(w)
        k = bool(k)
        d = bool(d)
        grSim_robot_command =  grSim_Commands_pb2.grSim_Robot_Command(id=robot_id, 
            kickspeedx=(self.kick_speed_x*k), kickspeedz=(self.kick_speed_z*k), 
            veltangent=vx, velnormal=vy, velangular=w, 
            spinner=d, wheelsspeed=self.wheel_speed)
        return grSim_robot_command
    
    def _commands_wrapper(self,is_yellow,grSim_robot_command) -> object:
        grSim_commands = grSim_Commands_pb2.grSim_Commands(timestamp=time.time(),
                                                           isteamyellow=is_yellow,
                                                           robot_commands=[grSim_robot_command])
        return grSim_commands
    
    def new_command(self,robot_id,vx,vy,w,k,d,us=True):
        grSim_robot_command = self._robot_command_wrapper(robot_id,vx,vy,w,k,d)
        grSim_commands = self._commands_wrapper(self.team(us),grSim_robot_command)
        return grSim_commands
    
    def convert(self,robot_commands:RobotCommand,us=True) -> None:
        grSim_commands = self.new_command(robot_id=robot_commands.robot_id,
            vx=robot_commands.vx,vy=robot_commands.vy,w=robot_commands.w,
            k=robot_commands.kick,d=robot_commands.dribble,us=us)
        return grSim_commands

    def pack(self,grSim_commands) -> bytes:
        grSim_packet = grSim_Packet_pb2.grSim_Packet(commands=grSim_commands)
        byte_packet = grSim_packet.SerializeToString()
        return byte_packet


# Test run
if __name__ == "__main__":
    # initialise this handler 
    isYellow = True
    GSC = GrSimRobotCommands(isYellow=isYellow) #always initialise this
    
    # building a new command from scratch 
    msg1 = GSC.new_command(robot_id=1,vx=2.0,vy=1.0,w=1,k=1,d=1,us=True)
    print(msg1)
    # to convert it to be ready to be sent :
    encoded = GSC.pack(msg1)
    print(encoded)
    # this should give you a bytes string for sending 
    
    
    # if you want to convert from
    r1 = RobotCommand(1,2,3,4,1,0) 
    msg2 = GSC.convert(r1)
    # afterwards, you can pack and send it ! no problem
    encoded = GSC.pack(msg2)
    print(msg2,encoded)

    
    # To check what the current team has set to use either one 
    isYellow = GSC.team(us=True)
    print(f"1. {isYellow=}")
    isYellow = GSC.isYellow
    print(f"2. {isYellow=}")
    
    # To update it's team color use either: 
    GSC.isYellow = not(isYellow)
    print(f"{isYellow=},{GSC.isYellow=}")
    
    GSC.update_is_yellow(not(isYellow))
    print(f"{isYellow=},{GSC.isYellow=},{GSC.team(us=True)=}")
    
    ## This packet is a one way packet ##