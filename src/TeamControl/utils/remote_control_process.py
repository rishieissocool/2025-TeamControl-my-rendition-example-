from TeamControl.world.model import WorldModel
from TeamControl.SSL.vision.frame import Frame
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot_behaviour.Movement import RobotMovement
from TeamControl.SSL.grSim.commands import GrSimRobotCommands
# from TeamControl.robot.robot_commands import RobotCommands
from TeamControl.network import grSimSender,Sender,RobotCommand

import pygame
import time

class RCProcess():
    def __init__(self, wm:WorldModel):
        self.us_yellow = False
        self.wm:WorldModel = wm
        self.last_version = 0
        robot_ip = ""
        self.sender = Sender(ip=robot_ip,port=50514)
        
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        self.loop()
        
    def loop(self):
        self.robot_id =2
        robot_pos = None
        last_update = time.time()
        while True:
            vx,vy,vw,k,d = 0,0,0,0,0

            current_version:int = self.wm.get_version()
            # print(current_version)
            if current_version > self.last_version:
                # print(f"{time.time() - last_update}, {self.wm.get_latest_frame().frame_number}")
                last_update = time.time()
                self.last_version = current_version
                robot_pos = self.wm.get_yellow_robots(isYellow=False,robot_id=self.robot_id).position
                # ball = self.wm.get_latest_frame().ball.position
            
            command = self.run_remote_control()
            if command.vx == 0 and command.vy == 0 and command.w ==0:
                command = None
            if command is not None:
                self.sender.send(command)

            if robot_pos is not None:
                # pos_relative_to_robot = world2robot(robot_position=robot_pos, target_position=ball)
                
                # vx,vy,w= RobotMovement.velocity_to_target(robot_pos=robot_pos,target=ball)
                # w = RobotMovement.turn_to_target(pos_relative_to_robot,speed=2)
                print(robot_pos)

    
        


    def run_remote_control(self):
        speed = 1

        vx,vy,vw,k,d = 0,0,0,0,0
        pygame.event.pump()  # Process internal events

        keys = pygame.key.get_pressed()  # Get key states
        if keys[pygame.K_ESCAPE]:  # Close the program
                pass
                
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
        
        return RobotCommand(robot_id=self.robot_id,vx=vx,vy=vy,w=vw,kick=k,dribble=d)