import pygame

from TeamControl.Network.Sender import Sender
from TeamControl.Coms.Action import Action

class Remote_robot():
    def __init__(self):
        robot_ip = "172.20.10.3"
        self.sender = Sender(ip=robot_ip,port=50514)
        
        self.us_yellow = True 


    def run_remote_control(self):
        robot_id = int(input("Enter the ID of Robot you want to control: "))
        speed = 100
        vx,vy,vw,k,d = 0,0,0,0,0
        # dribbler_on = False
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        running = True
        while running:
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
                vx = vx*100
                vy = vy*100
                vw = vw*5
                
            if keys[pygame.K_f]:
                k = 1
            # if keys[pygame.K_r]: #chip kick
            #     k = 2
            if keys[pygame.K_SPACE]:    
                d = 1
            
                                            
            action = Action(robot_id=robot_id, vx=vx,vy=vy,w=vw,kick=k,dribble=d)
            vx,vy,vw,k,d = 0,0,0,0,0
            self.sender.send_action(action)

if __name__ == "__main__":
    rc = Remote_robot()
    rc.run_remote_control()