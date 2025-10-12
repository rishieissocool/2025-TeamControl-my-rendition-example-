

from TeamControl.network.robot_command import RobotCommand
from TeamControl.world.transform_cords import world2robot
from TeamControl.robot.Movement import RobotMovement
from TeamControl.utils.Logger import LogSaver 

from TeamControl.world.model import WorldModel
from TeamControl.SSL.vision.frame import Frame
from multiprocessing import Queue

import time
class RCProcess():
    def __init__(self, dispatch_q:Queue, 
                 wm:WorldModel,
                 robot_id:int,
                 us_yellow=True):
        self.wm:WorldModel = wm
        self.dispatch_q = dispatch_q
        self.robot_id = robot_id
        self.us_yellow = us_yellow
        self.last_version = 0
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
            # puts command into queue
            self.dispatch_q.put(cmd,5) # 5 seconds runtime
                
                

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
                # puts command into queue
                self.dispatch_q.put(msg,5) # 5 seconds runtime
        
    
    
def run_rc_process(dispatch_q,wm:WorldModel,robot_id,is_yellow):
    dummy = RCProcess(dispatch_q, wm=wm,robot_id=robot_id,us_yellow=is_yellow)
    dummy.run()
