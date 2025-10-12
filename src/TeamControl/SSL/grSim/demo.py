## how to run stuff to send to grSim ### 
## 1. create the socket for recving and sending
from TeamControl.network.ssl_sockets import *



destination_ip = "127.0.0.1" 
command_listening_port = 20010
sender = grSimSender(ip=destination_ip , port=command_listening_port ,is_yellow=isYellow)

def example_1(sender):
    msg1 = sender.new_raw_command(robot_id=1,vx=2.0,vy=1.0,w=1,k=1,d=1,us=True)
    print(msg1) 
    # sends the message
    sender.send(msg1) 

    encoded = GSC.encode(msg1) #can encode first then send
    sender.send(encoded)
    
def example_2(sender):
    r1 = RobotCommand(robot_id=1,vx=2,vy=3,w=4,k=1,d=0) 
    sender.send_command(r1)
    print(msg2,encoded)
