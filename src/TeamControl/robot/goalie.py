from TeamControl.network import Sender, RobotCommand,grSimSender
from TeamControl.world.Trajectory import predict_trajectory
from TeamControl.world.transform_cords import world2robot
from TeamControl.voronoi_planner.voronoi_planner import VoronoiPlanner
from TeamControl.robot.Movement import RobotMovement
 

# typings
from TeamControl.world.model import WorldModel
from TeamControl.SSL.vision.frame import Frame


class Goalie():
    def __init__(self,wm:WorldModel,goalie_id,goalie_ip):
        self.is_yellow = True
        self.is_positive = True
        self.id = goalie_id
        self.ip = goalie_ip
        # self.sender = Sender(ip=goalie_ip,port=50514)
        self.sender = grSimSender(is_yellow=self.is_yellow)
        self.wm = wm
        self.ball_hist =list()
        self.planner =VoronoiPlanner(xsize=9000,ysize=6000)
        self.version = 0
        self.field_x = 9000 
        self.field_y = 6000
        self.goal_depth = 200
        self.neutral_x_pos = self.field_x/2-self.goal_depth if self.is_positive else -(self.field_x/2-self.goal_depth)

    def test(self):
        pass
    
    def run(self):            
        while True:     
            # if self.version <= self.wm.get_version():
            try:
                self.wm.get_yellow_robots(isYellow=self.is_yellow,robot_id=self.id)
                self.ball_hist = self.update_ball_history(5)
                # print("ball history has been updated")
            except AttributeError:
                continue
            
            goalie_points = predict_trajectory(self.ball_hist, 3, isPostive=self.is_positive, feild_size=(self.field_x,self.field_y))
            # goalie_points = predict_trajectory(self.ball_hist, 3, isPostive=self.is_positive, feild_size=(4800, 2700))
        
            goalie_pos = self.wm.get_yellow_robots(isYellow=self.is_yellow,robot_id=self.id).position
            
            if goalie_points[1] == True:              
                target_pos1 = world2robot(robot_position=goalie_pos,target_position=goalie_points[0])
            else: #reset position
                # target_pos1 = world2robot(robot_position=goalie_pos,target_position= (2200, 0))
                target_pos1 = world2robot(robot_position=goalie_pos,target_position= (self.neutral_x_pos, 0))
                
            print("Relative Target : ", target_pos1)
            # target_pos = world2robot(robot_position=robot_pos,target_position=target)
            # # print(target)
            vx1,vy1 = RobotMovement.go_To_Target(target_pos=target_pos1, stop_threshold=50)
            # w1 = RobotMovement.turn_to_target(target_pos2)
            # w = 0 
    
            command1 = RobotCommand(robot_id=self.id,vx=vx1,vy=vy1)
            
            self.sender.send_command(command1)
        
            # player_pos = vision_sock.world_model.get_our_robot(robot_id=Player_id)
            # print(f"{player_pos=}")
            # # target = ball_pos
            
            # target_pos2 = world2robot(robot_position=player_pos,target_position=ball_pos)
            # print("Relative Target : ", target_pos2)
            # # target_pos = world2robot(robot_position=robot_pos,target_position=target)
            # # # print(target)
            # vx2,vy2 = RobotMovement.go_To_Target(target_pos=target_pos2)
            
            # action2 = Action(robot_id=goalie_id,vx=vx2*40,vy=vy2*40)
            # # # print(action)   
            # sender1.send_action(action=action1,destination=(goalie_ip,robot_port))
            # sender2.send_action(action=action2,destination=(player_ip,robot_port))
            
            # start_time = time.time()
    def update_ball_history(self,n:int):
        self.ball_hist = list()
        frames = self.wm.get_last_n_frames(n)
        l = len(frames)
        for i in range(l):
            ball_data = frames[i].ball
            if ball_data != None:
                # print(ball_data)
                self.ball_hist.append([ball_data.x,ball_data.y])
        # print(len(self.ball_hist))
        return self.ball_hist
        
    
def run_goalie(wm: WorldModel,goalie_id,goalie_ip="127.0.0.1"):
    g = Goalie(wm,goalie_id=goalie_id,goalie_ip=goalie_ip)
    g.run()