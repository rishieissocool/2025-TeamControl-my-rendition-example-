from TeamControl.world.model import WorldModel
from TeamControl.SSL.vision.frame import Frame
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot_behaviour.Movement import RobotMovement
from TeamControl.SSL.grSim.commands import GrSimRobotCommands
from TeamControl.robot.robot_commands import RobotCommands
from TeamControl.network.grSimSockets import grSimSender


import time

class DummyReader():
    def __init__(self, wm:WorldModel):
        self.wm:WorldModel = wm
        self.last_version = 0
        self.sender = grSimSender(isYellow=True)
        self.loop()
        
    def loop(self):
        robot_id =1
        robot_pos = None
        last_update = time.time()
        while True:
            current_version:int = self.wm.get_version()
            # print(current_version)
            if current_version > self.last_version:
                # print(f"{time.time() - last_update}, {self.wm.get_latest_frame().frame_number}")
                last_update = time.time()
                self.last_version = current_version
                robot_pos = self.wm.get_yellow_robots(isYellow=True,robot_id=robot_id).position
                ball = self.wm.get_latest_frame().ball.position
            
            if robot_pos is not None:
                pos_relative_to_robot = world2robot(robot_position=robot_pos, target_position=ball)
                
                vx,vy,w= RobotMovement.velocity_to_target(robot_pos=robot_pos,target=ball)
                # w = RobotMovement.turn_to_target(pos_relative_to_robot,speed=2)
                print(vx,vy,w)
            
                cmd = RobotCommands(robot_id=robot_id,vx=vx,vy=vy,w=w,kick=0,dribble=0)
                cmd = self.GSC.convert(cmd)
                encoded = self.GSC.pack(cmd)
                self.sender.send(encoded)