import pygame

from TeamControl.network import Sender,grSimSender
from TeamControl.network.robotCommand import RobotCommand

class Remote_robot():
    def __init__(self,use_sim:bool=False,isYellow=True):
        self.us_yellow = isYellow
        if use_sim is True:
            device_ip = "127.0.0.1"
            DEFAULT = 20010
            self.sender = grSimSender(isYellow=isYellow,ip=device_ip,port=DEFAULT)
        elif use_sim is False:
            robot_ip = "192.168.70.56"
            self.sender = Sender(ip=robot_ip,port=50514)
        


    def run_remote_control(self):
        robot_id = int(input("Enter the ID of Robot you want to control: "))
        speed = 1
        vx,vy,vw,k,d = 0,0,0,0,0
        # dribbler_on = False
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        running = True
        while running:
            vx,vy,vw,k,d = 0,0,0,0,0
            pygame.event.pump()  # Process internal events

            keys = pygame.key.get_pressed()  # Get key states
            if keys[pygame.K_ESCAPE]:  # Close the program
                    running = False
                    
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
            
                                            
            Command = RobotCommand(robot_id=robot_id, vx=vx,vy=vy,w=vw,kick=k,dribble=d)
            if Command.vx == 0 and Command.vy == 0 and Command.w ==0:
                continue # skips the command send
            
            self.sender.send(Command)


if __name__ == "__main__":
    rc = Remote_robot()
    rc.run_remote_control()