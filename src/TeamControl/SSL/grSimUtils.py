"""
This class is going to be replaced. 
"""
import time
# from pynput.keyboard import Key, Listener

from TeamControl.Model.world import World as wm
from TeamControl.Coms.grSimAction import grSim_Action
from TeamControl.Network.ssl_networking import grSimVision, grSimSender
from TeamControl.RobotBehaviour.goToTarget import *
from TeamControl.Model.transform_cords import *

TIME = time.time()
class grSimUtils():
    """This is the main / sandbox class for grSim Control
    This class has a world_model, receiver and sender
    """
    def __init__(self,isYellow : bool, isPositive : bool ,ip:str = '127.0.0.1', vision_port : int=10020, sender_port : int=20011) -> None:
        """Initalising GRSIM Tools. 
        This includes : 
        GRSIM VISION
        GRSIM Command Sender

        Args:
            isYellow (bool): Do you want your Team Color to be Yellow
            isPositive (bool): Are you on the Positive half of the field
            ip (str): The IP of the device you trying to communicate to, the GRSIM Device IP
            vision_port (int): GRSIM Vision port number. Default : 10020 or 10006
            sender_port (int): grSim Command listening Port Number.
        """
        self.us_yellow = isYellow
        self.us_positive = isPositive
        self.world_model = wm(isYellow=self.us_yellow, isPositive=self.us_positive)
        self.vision = grSimVision(world_model=self.world_model,port=vision_port)
        self.sender = grSimSender(ip=ip, port=sender_port)
        
        
    def get_team_color(self,ourTeam):
        if ourTeam is True:
            return self.us_yellow
        elif ourTeam is False:
            return not(self.us_yellow)
    
        
            
    # some simple functions
    def make_robot_move(self,ourTeam: bool,robot_id:int,vx=0.0,vy=0.0,vw=0.0):
        isYellow = self.get_team_color(ourTeam)
        action = grSim_Action(isYellow=isYellow,robot_id=robot_id,vx=vx,vy=vy,w=vw)
        self.sender.send_action(action)
      
    
    def make_robot_kick(self, ourTeam:bool, robot_id:int, kickx = 1.0, kickz = 0.0):
        isYellow = self.get_team_color(ourTeam)
        action = grSim_Action(isYellow=isYellow,robot_id=robot_id,kx=kickx,kz=kickz)
        self.sender.send_action(action)

    def make_robot_dribble(self,ourTeam:bool,robot_id:int, dribble: bool):
        isYellow = self.get_team_color(ourTeam)
        action = grSim_Action(isYellow=isYellow,robot_id=robot_id,d=dribble)
        self.sender.send_action(action)
        
    def run_remote_control(self):
        robot_id = int(input("Enter the ID of Robot you want to control: "))
        self.us_yellow = True 
        speed = 5.0
        vx,vy,vw,k,d = 0,0,0,0,0
        # dribbler_on = False
        import pygame
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
            if keys[pygame.K_r]:
                k = 2
            if keys[pygame.K_SPACE]:    
                d = 1
            
                                            
            action = grSim_Action(isYellow=self.us_yellow, robot_id=robot_id, vx=vx,vy=vy,w=vw,kick=k,dribble=d)
            vx,vy,vw,k,d = 0,0,0,0,0
            self.sender.send_action(action)
    
    def run_code(self):
        action_list = list()
        robot_id = int(input("Enter the ID of Robot you want to control: "))
        while True:
            
            world_model_fully_updated = self.vision.listen()
            if world_model_fully_updated is True :
                target = self.world_model.get_ball()
                robot_pos = self.world_model.get_our_robot(robot_id)
                print(f'{target=}')
                print(f'{robot_pos=}')
                translated_point = self.world2Robot(robot_pos,target)
                print(f'{translated_point=}')
                vx,vy = go_To_Target(translated_point)
                w = turn_to_target(translated_point)
                action = self.make_robot_move(ourTeam=True,robot_id=robot_id,vx=vx,vy=vy,vw=w)
                action_list.append(action)
    
            if len(action_list) > 0:
                a = action_list.pop(0)
                self.sender.send_action(isYellow=self.ourTeam,action=a)
    

if __name__ =="__main__" :
    controller = grSimUtils(isPositive=True, isYellow=False)
    controller.run_remote_control()