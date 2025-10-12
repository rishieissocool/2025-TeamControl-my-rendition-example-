
# from TeamControl.SSL.grSim.commands import GrSimRobotCommands
# from TeamControl.robot.robot_commands import RobotCommands
from TeamControl.network.robotCommand import RobotCommand
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot.Movement import RobotMovement
from TeamControl.utils.Logger import LogSaver 

from TeamControl.world.model import WorldModel
from TeamControl.SSL.vision.frame import Frame
from TeamControl.network import Sender,grSimSender

import time
class RCProcess():
    def __init__(self, wm:WorldModel,robot_id:int,
                 robot_ip:str="127.0.0.1",us_yellow=True):
        self.robot_id = robot_id
        self.us_yellow = us_yellow
        self.wm:WorldModel = wm
        self.last_version = 0
        self.sender = Sender(ip=robot_ip,port=50514)
        self.logs = LogSaver(process_name="rc_Process",id=robot_id)

        
        
    def run(self):
        if self.robot_id is None:
            self.logs.error("ROBOT ID IS NONE EXITING . . .")
        last_update = time.time()
        vx,vy,w,k,d = 0,0,0,0,0
        while True:

            current_version:int = self.wm.get_version()
            # print(current_version)
            if current_version > self.last_version:
                self.logs.debug(f"{time.time() - last_update}, {self.wm.get_latest_frame().frame_number}")
                last_update = time.time()
                self.last_version = current_version
                try:
                    robot_pos = self.wm.get_yellow_robots(isYellow=False,robot_id=self.robot_id).position
                    ball = self.wm.get_latest_frame().ball.position
                except Exception :
                    robot_pos = 0,0,0
                    ball = 0,0
                    
                vx, vy, w= RobotMovement.velocity_to_target(robot_pos=robot_pos, target=ball)
                
            cmd = RobotCommand(1, vx, vy, w, 0, 0)
            self.logs.info(cmd)
            self.sender.send(cmd)
                
                
            
            # command = self.run_remote_control()
            # if command.vx == 0 and command.vy == 0 and command.w ==0:
            #     command = None
            # if command is not None:
            #     self.sender.send(command)

            # if robot_pos is not None:
                # pos_relative_to_robot = world2robot(robot_position=robot_pos, target_position=ball)
                
                # vx,vy,w= RobotMovement.velocity_to_target(robot_pos=robot_pos,target=ball)
                # w = RobotMovement.turn_to_target(pos_relative_to_robot,speed=2)
                # print(robot_pos)

        


    def run_remote_control(self):
        import pygame
        
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        
        speed = 1
        while True:
            vx,vy,vw,k,d = 0,0,0,0,0
            pygame.event.pump()  # Process internal events

            keys = pygame.key.get_pressed()  # Get key states
            if keys[pygame.K_ESCAPE]:  # Close the program
                    break
                    
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                vx += +speed
                
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                vx += -speed    
                
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if self.us_yellow is True:
                    vy += +speed    
                elif self.us_yellow is False:
                    vy += -speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if self.us_yellow is True:
                    vy += -speed    
                elif self.us_yellow is False:
                    vy += +speed
                
            if keys[pygame.K_q] or keys[pygame.K_PAGEUP]:
                vw += +speed
            if keys[pygame.K_e] or keys[pygame.K_PAGEDOWN]:
                vw += -speed
            
            
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                vx = vx*10
                vy = vy*10
                vw = vw*5
                
            if keys[pygame.K_f]:
                k = 1
            # if keys[pygame.K_r]: #chip kick
            #     k = 2
            if keys[pygame.K_SPACE]:    
                d = 1
            
            if vx !=0 or vy != 0 or vw!=0 or k !=0 or d!=0:
                
                msg = RobotCommand(robot_id=self.robot_id,vx=vx,vy=vy,w=vw,kick=k,dribble=d)
                encoded_msg = msg.encode()
                self.logs.info(f"sent {msg=}")
                self.sender.send(encoded_msg)
    
    
def run_rc_process(wm:WorldModel):
    dummy = RCProcess(wm=wm,robot_id=1)
    dummy.run()
    
if __name__ == "__main__":
    wm = WorldModel()
    run_rc_process(wm)