from TeamControl.network.robot_command import RobotCommand
from TeamControl.robot.Movement import RobotMovement

from TeamControl.world.Trajectory import predict_trajectory
from TeamControl.world.transform_cords import world2robot
# from TeamControl.voronoi_planner.voronoi_planner import VoronoiPlanner
 
# typings
from TeamControl.world.model import WorldModel
from TeamControl.SSL.vision.frame import Frame
from multiprocessing import Queue


class Goalie():
    def __init__(self,dispatch_q:Queue,wm:WorldModel,goalie_id,is_yellow):
        self.dispatch_q = dispatch_q
        self.is_yellow = is_yellow
        self.wm = wm
        self.id = goalie_id
        self.version = 0
        self.field_x = 9000 
        self.field_y = 6000
        self.goal_depth = 200
        self.is_positive = True
        self.ball_hist =list()
        self.neutral_x_pos = self.field_x/2-self.goal_depth if self.is_positive else -(self.field_x/2-self.goal_depth)

    def test(self):
        pass
    
    def run(self):            
        while True:     
            # if self.version <= self.wm.get_version():
            try:
                self.wm.get_yellow_robots(isYellow=self.is_yellow,robot_id=self.id)
                self.ball_hist = self.update_ball_history(5)
            except AttributeError:
                continue
            
            goalie_points = predict_trajectory(self.ball_hist, 3, isPostive=self.is_positive, feild_size=(self.field_x,self.field_y))
        
            goalie_pos = self.wm.get_yellow_robots(isYellow=self.is_yellow,robot_id=self.id).position
            
            if goalie_points[1] == True:   
                # if there's a point go block           
                target_pos1 = world2robot(robot_position=goalie_pos,target_position=goalie_points[0])
            else: #reset position
                target_pos1 = world2robot(robot_position=goalie_pos,target_position= (self.neutral_x_pos, 0))
                
            print("Relative Target : ", target_pos1)
            vx1,vy1 = RobotMovement.go_To_Target(target_pos=target_pos1, stop_threshold=50)
           
    
            command1 = RobotCommand(robot_id=self.id,vx=vx1,vy=vy1)
            # puts command into queue
            self.dispatch_q.put(command1,5) # 5 seconds runtime
        
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
        
    
def run_goalie(dispatch_q,wm: WorldModel,goalie_id,is_yellow):
    g = Goalie(dispatch_q,wm,goalie_id=goalie_id,is_yellow=is_yellow)
    g.run()