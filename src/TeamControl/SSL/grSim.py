from TeamControl.SSL.proto2 import *
from TeamControl.Model.world import World as wm
from TeamControl.Network.Receiver import *
from TeamControl.Network.Sender import *
from TeamControl.Network.Robot import *
from TeamControl.Model.frame import Robot as r
from TeamControl.RobotBehaviour.goToTarget import *
from TeamControl.Model.transform_cords import *
from TeamControl.Formation.relative_position import *
from sklearn.linear_model import LinearRegression
from TeamControl.RobotBehaviour.behaviour import *

class grSimServer():
    def __init__(self,isYellow:bool, isPositive:bool, ip:str = None, isPostive = False): 
        self.world_model = wm(isYellow=isYellow, isPositive = isPositive,max_cameras=4)
        self.vision_sock = grSimVision(world_model=self.world_model, ip=ip)
        self.feild_size = (9000,6000)
        self.sender = grSimSender()
        self.isYellow = isYellow
        self.isPostive = isPostive
        self.positions = activeFormation(self.world_model,self.isPostive, self.feild_size)
        self.behaviour = RobotMovement()
        self.isPositive = isPositive
        # self.SimControl = grSimControl()
        # self.YellowControl = grSimYellowControl()
        # self.BlueControl = grSimBlueControl()

    def action(self, list_action : list):
        for action in list_action:
            if isinstance(action,grSim_Action) and not None:
                self.sender.send_action(action)
            # print(f"SENT : {action=}")
    
    def run():
        ...
    
    def all_To_Target(self,target_pos):
        for id in range(6):
            pos = self.world_model.get_our_robot(id)
            # print(target)
            tag = world2robot(pos, target_pos)
            vx,vy = go_To_Target(tag)
            w = turn_to_target(tag)
            action = grSim_Action(isYellow=isYellow,robot_id=id,vx=vx,vy=vy,w=w)
            list_action.append(action)
        return list_action
        
    def formation(self,ball_pos, robot_ids):
        for id in robot_ids:
                robot_pos = self.world_model.get_our_robot(robot_id=id)
                if robot_pos is None:
                    print(f'========>{id}')
                    print(f'========>{robot_pos}')
                    continue
                target = self.positions.formation_212_pos(player_no=id, ball_pos= ball_pos)
                
                vx, vy, w = behaviour.velocity_to_target(robot_pos, target)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                action = grSim_Action(isYellow,id, vx,vy,w)
                list_action.append(action)
        return list_action

    
    def friendly_proximity(self, target_pos) -> list[int, float]:
        '''
        input:
        all robots ids and ball position 

        output:
        sorted_list: distnace of all our robot to the ball ordered form closest to futherest
        '''
        diff_list = []

            # sets the robot position in x and y coordintes 
        all_enemy_robot_objects = server.world_model.get_our_robot(None,format=r.SELF)
        for pos in all_enemy_robot_objects:
            diff = np.sqrt((pos.x-target_pos[0])**2 +(pos.y-target_pos[1])**2)
            diff_list.append([pos.id,diff])
        sorted_list = sorted(diff_list, key = lambda x: x[1])
        
        
        return sorted_list
    
    def enemy_proxmity(self, target_pos):
        
        diff_list = []

        
            # sets the robot position in x and y coordintes 
        all_enemy_robot_objects = server.world_model.get_enemy_robot(None,format=r.SELF)
        for pos in all_enemy_robot_objects:
            diff = np.sqrt((pos.x-target_pos[0])**2 +(pos.y-target_pos[1])**2)
            diff_list.append([pos.id,diff])
        sorted_list = sorted(diff_list, key = lambda x: x[1])
        
        
        return sorted_list
    
    def blocking_pos(self, enemy_pos, buffer = 500):

        '''
        Input:
        Enemy ID that you want to block
        buffer: how far you want our robot to be in front of the enemy
        
        Output:
        The x and y pos the the robot has to be in to block the enemy
        '''


        enemy_oreantation = enemy_pos[2]

        block_pos_x = buffer*np.cos(enemy_oreantation) + enemy_pos[0]
        block_pos_y = buffer*np.sin(enemy_oreantation) + enemy_pos[1]

        block_pos = [block_pos_x, block_pos_y]

        return block_pos
    
    def treg_ball(self,ball_his, feild_size):
        # PARAMETERS
        #GOALIE_LINE = -FIELD_LENGTH/2 + 200 #mm #On the other side of the field if we are the other team
        goal_width = 1000 # the width of the goal 
        # currently yellow is set as right side and blue set as felt side 
        playing_side = self.isPositive
        if playing_side == True:
            goal_pos = (4200,0)
        else:
            goal_pos = (-4200,0)

        goal_line = goal_pos[0]
        num_samples = 5
        #print(ball_pos)
        ball_pos_x = []
        ball_pos_y = []
        for ball_pos in ball_his:
            ball_pos_x.append(ball_pos[0])
            ball_pos_y.append(ball_pos[1])
        if len(ball_pos) <= num_samples:
            # use all available ball positions
            last_ball_positions_x = ball_pos_x
            last_ball_positions_y = ball_pos_y
        
            # print(ball_pos_x)
            # print(ball_pos_y)
        else:
            # use last num_samples ball positions
            last_ball_positions_x = ball_pos_x[-num_samples:]
            last_ball_positions_y = ball_pos_y[-num_samples:]
        
        # print(last_ball_positions_x)1
        # print(last_ball_positions_y)
      

        model = LinearRegression()
        model.fit(np.array(last_ball_positions_x).reshape(-1, 1), last_ball_positions_y)

            # Generate trajectory points
        x_values = np.linspace(-feild_size[0]/2, feild_size[0]/2, 20) 

        current_ball_position_x = ball_pos_x[-1]  # Current ball positionn

        trajectory_y_at_goal_line = model.predict(np.array([goal_line]).reshape(-1, 1))
            
        intersect_line = -goal_width / 2 <= abs(trajectory_y_at_goal_line) <= goal_width/ 2
        # Calculate intersection point if exists
            
        goalie_pos = (goal_line, round(trajectory_y_at_goal_line.item()))
        return goalie_pos, intersect_line
    

        
    
    
    



if __name__ == "__main__":

    print("is your team Yellow ? : [y/n]")
    ans = input()
    if ans == "y":
        isYellow = True
        isPostive = True
        isPositive = True
    else :
        isYellow = False
        isPostive = False
        isPositive = False
    server = grSimServer(isYellow,isPositive, isPostive=isPostive)
    behaviour = server.behaviour
    formation = server.positions
    
    while True: 
        list_action = list()
        updated = server.vision_sock.listen()
        if updated:
            #Gets the ball Position 
            ball_pos = server.world_model.get_ball()
            
            all_ball_history = server.world_model.get_ball(hist = True)
            ball_history = all_ball_history[:5]
            # print(f"ball history is {ball_history}")
            # setting id for the robots on the feild 
            goalie_id = 0
            id = server.world_model.get_our_ids()
            id.remove(goalie_id)
            print(f'{id=}')
            enemy_ids = server.world_model.get_enemy_ids()
            # gets a list of action the fromation function uses
            print(id)
            # #sets the defult formation of the robots 
            list_action = server.formation(ball_pos, id)
            # # we get proxmity of all our robots to the ball 
            # gaolie ============================================
            
            
            goalie_position = server.world_model.get_our_robot(goalie_id)
            
            print(goalie_position)
            goalie_pos, intersect_line = server.treg_ball(ball_history,(9000, 6000))
    
            
            
            if intersect_line:
                goalie_target = goalie_pos
            else:
                goalie_target = formation.golaie_pos(ball_pos)

                 
            
            gx, gy, gw = behaviour.velocity_to_target(goalie_position, goalie_target, ball_pos)
            
            goalie_action = grSim_Action(isYellow, goalie_id, gx, gy, gw)
            
            list_action.append(goalie_action)
            
            # # Golaie ===========================================
            
            
            list_our_prox2ball = server.friendly_proximity(ball_pos)
            list_enemy_prox2ball = server.enemy_proxmity(ball_pos)
            
            closest_enemy_id,closest_enemy_dist = list_enemy_prox2ball[0]
            closest_player_id,closest_player_dist = list_our_prox2ball[0]
            # # # we get the clostest player 
            # print(f"{list_enemy_prox2ball=}")
            
            
            
            
            
            
            if closest_enemy_dist < 500:
            #         #get the enemy position
                close_enemy_pos = server.world_model.get_enemy_robot(closest_enemy_id)
            #         # gets our all our robot proxmity to enemy
                defender_prox = server.friendly_proximity(close_enemy_pos)
                #print(f'{defender_prox=}')
            #         # gets the id of the clostest defender
                closest_defender_id = defender_prox[0][0]
            #         # gets our defender position
                defender_pos = server.world_model.get_our_robot(closest_defender_id)
                    #gtes the position which blocks the emeny view 
                blocking_pos = server.blocking_pos(close_enemy_pos)
                    # getting the velocity needed to reach the defensive position 
                dx, dy, dw = behaviour.velocity_to_target(defender_pos, blocking_pos, (close_enemy_pos[0], close_enemy_pos[1]))
                    # the action the defender has to do to block the enemy 
                blocking_action = grSim_Action(isYellow, closest_defender_id, dx, dy, dw)
                    #adds it to the action list 
                list_action.append(blocking_action) 
            else:
                # if ball if too far, we hve a chaser whoes id is the clostest robot to the ball 
                ball_chaser_id = closest_player_id
                if closest_player_id == goalie_id:
                    ball_chaser_id = list_our_prox2ball[1][0]
                ball_chaser = server.world_model.get_our_robot(ball_chaser_id)
                
                if closest_player_dist < 50:
                    enemy_goal_pos = (4200, 0)
                    chaser_target = enemy_goal_pos
                    cx, cy, cw = behaviour.velocity_to_target(ball_chaser, chaser_target, stop_threshold=50)
                else:
                    cx, cy, cw = behaviour.velocity_to_target(ball_chaser, ball_pos, stop_threshold=50)
                # gets the velocity required for the chaser 
                # sets it into action then into the list of action 
                chaser_action = grSim_Action(isYellow, ball_chaser_id, cx, cy, cw)
                
                
                    
                list_action.append(chaser_action)
            
                
            
            
            
            
            server.action(list_action)
        
            
            

