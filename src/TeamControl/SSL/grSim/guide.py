## this is here as assist. 

## Normal command sending : 

from TeamControl.network.robotCommand import RobotCommand
from TeamControl.network.sender import Sender
from TeamControl.network.receiver import Receiver
def send_command():
    command = RobotCommand(robot_id=1,vx=1,vy=1,w=0,kick=0,dribble=0)
    encoded = command.encode()
    server = Sender()
    server.send(encoded,port=50514)
    
def recv_command():
    recv = Receiver(port=50514)
    msg,_ = recv.listen()
    decoded_msg = RobotCommand.decode(msg)
    print(f"RECEIVED : {decoded_msg}")

# grSim operation
from TeamControl.SSL.grSim.commands import GrSimRobotCommands
from TeamControl.SSL.grSim.grSimSockets import grSimSender
def send_grsim_command():
    team_is_yellow = True
    host = GrSimRobotCommands(isYellow=team_is_yellow)
    command = host.new_command(robot_id=1,vx=1,vy=1,w=1,k=0,d=0)
    packed_command = host.pack(command)
    sender = grSimSender()
    sender.send_command(packed_command)

def send_to_grsim_command():
    team_is_yellow = True
    host = GrSimRobotCommands(isYellow=team_is_yellow)
    command = RobotCommand(robot_id=1,vx=1,vy=1,w=0,kick=0,dribble=0)
    grsim_command = host.convert(command)
    packed_command = host.pack(grsim_command)
    sender = grSimSender()
    sender.send_command(packed_command)
    