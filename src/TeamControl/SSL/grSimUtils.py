"""
This class is going to be replaced. 
"""
import time
# from pynput.keyboard import Key, Listener

from TeamControl.Model.world import World as wm
from TeamControl.Coms.grSimAction import grSim_Action
from TeamControl.Network.Sender import grSimSender
from TeamControl.Network.Receiver import grSimVision

TIME = time.time()
class grSimUtils():
    """This is the main / sandbox class for grSim Control
    This class has a world_model, receiver and sender
    """
    def __init__(self,isYellow) -> None:
        self.set_team_color(isYellow)
        self.world_model = wm(isYellow=isYellow)
        self.receiver = grSimVision(self.world_model,ip= None)
        self.sender = grSimSender()
        
    def set_team_color(self,isYellow):
        self.ourTeam = isYellow
        self.enemyTeam = not(isYellow)    
        
    def get_team_color(self,ourTeam):
        if ourTeam is True:
            return self.ourTeam
        elif ourTeam is False:
            return self.enemyTeam
        
    def send_action(self,action:grSim_Action):
        self.sender.send_action(action)
        
        
    # some simple functions
    def robot_move(self,ourTeam: bool,robot_id:int,vx=0.0,vy=0.0,vw=0.0):
        isYellow = self.get_team_color(ourTeam)
        action = grSim_Action(isYellow=isYellow,robot_id=robot_id,vx=vx,vy=vy,w=vw)
        self.send_action(action)
      
    
    def robot_kick(self, ourTeam:bool, robot_id:int, kickx = 1.0, kickz = 0.0):
        isYellow = self.get_team_color(ourTeam)
        action = grSim_Action(isYellow=isYellow,robot_id=robot_id,kx=kickx,kz=kickz)
        self.sender.send_action(action)

    def robot_dribble(self,ourTeam:bool,robot_id:int, dribble: bool):
        isYellow = self.get_team_color(ourTeam)
        action = grSim_Action(isYellow=isYellow,robot_id=robot_id,d=dribble)
        self.sender.send_action(action)

    def keyboardMovements(self):
        speed = 1
        accel = 2
        vx = 0
        vy = 0
        w = 0
        kx = 0
        
        
        import keyboard # this module requires to be run in sudo
        msg = ""    
        if keyboard.is_pressed('shift'):
            speed = speed*accel
            msg+= 'fast as f boi'

        if keyboard.is_pressed('w'):
            msg+=' forward '
            vx = speed
        elif keyboard.is_pressed('s'):
            msg+=' backward '
            vx = -speed
        if keyboard.is_pressed('a'):
            msg+= ' left '
            vy = speed
        elif keyboard.is_pressed('d'):
            msg += ' right '
            vy = -speed
            
        if keyboard.is_pressed('q'):
            msg+= ' CCW '
            w = speed
        elif keyboard.is_pressed('e'):
            msg+= ' CW '
            w = -speed
        
        if keyboard.is_pressed("f"):
            msg+=" Kick "
            kx = 5
        
        if keyboard.is_pressed(" "):
            msg+=" dribble "
            dribble = True
        else:
            dribble = False
        
        print(msg)
        return vx,vy,w,kx, dribble

        # Collect events until released
         
       
        # from pynput.keyboard import Key, Listener

        # def on_press(key):
        #     #print('{0} pressed'.format(
        #         #key))
        #     check_key(key)

        # def on_release(key):
        #     #print('{0} release'.format(
        #     # key))
        #     if key == Key.esc:
        #         # Stop listener
        #         return False
        
        # def check_key(key):
        #     msg = ''

        #     if key.char == "w": 
        #         msg+=' forward '
        #         vx = speed
        #     elif key.char == 's':
        #         msg+=' backward '
        #         vx = -speed
            
        #     if key.char == "a": 
        #         msg+=' left '
        #         vy = speed
        #     elif key.char == 'd':
        #         msg+=' right '
        #         vy = -speed
            
        #     if key.char == "q": 
        #         msg+=' CCW '
        #         w = speed
        #     elif key.char == 'e':
        #         msg+=' CW '
        #         w = -speed
        # with Listener(
        #     on_press=on_press,
        #     on_release=on_release) as listener:
        #     listener.join()
        
        
            
    def hi(self,robot_pos,target):
        import numpy as np
        pos = robot_pos # x, y, fd
        print(pos)
        cos = np.cos(pos[2]) # cos(fd)
        sin = np.sin(pos[2]) # si(fd)

        transformation_matrix = np.array([
                [cos, -sin, pos[0]], #x
                [sin,  cos, pos[1]], #y
                [0,  0,    1] #w
            ])
        # print(f'{transformation_matrix=}')
        trans_matrix = np.linalg.inv(transformation_matrix) # 1/trans_matrix
        # print(f'{trans_matrix=}')
        target= np.append(target,1) # world (visionSSL) coordinate system
        # print(f'{target=}')
        translated_point = np.dot(trans_matrix, target)
        # translated_point = translated_point[:2]
        return translated_point
    # def robot_to_world():
        
    def run(self):
        robot_id = int(input("Enter the ID of Robot you want to control: "))

        while True:
            updated= self.receiver.listen()
            if updated is True :
                # # obtain target
                # target = self.world_model.get_ball()
                # robot_pos = self.world_model.get_our_robot(1)
                # print(f'{target=}')
                # print(f'{robot_pos=}')
                # translated_point = self.hi(robot_pos,target)
                # print(f'{translated_point=}')
                # self.keyboardMovements()
                
                # action = self.robot_move(True,1,0,1,0)
                # print(self.world_model.get_our_robot(1))
                vx,vy,w,kx,d = self.keyboardMovements()
                action = grSim_Action(isYellow=True,robot_id=robot_id,vx=vx,vy=vy,w=w,kx=kx,d=d)
                print(action)
                # sends action to robot
                self.send_action(action)

if __name__ =="__main__" :
    controller = grSimUtils(False)
    controller.run()