#a simple behaviour to update the blackboard with world model data
import py_trees
import time
from TeamControl.world.model import WorldModel
from TeamControl.world.nearest import Nearest
from TeamControl.world.Trajectory import predict_trajectory
from TeamControl.SSL.vision.frame import Robot
from TeamControl.Examples.blackboard import bb  

class BlackboardUpdater(py_trees.behaviour.Behaviour):

    def __init__(self, world, robots):
        super().__init__("BlackboardUpdater")
        self.world = world
        self.robots = robots

    def update(self):
        state = bb()  # from schema above
        state.tick_ts = time.time()
        state.robots = self.robots
        state.field_size = (self.world.field.x, self.world.field.y) if getattr(self.world, "field", None) else (9000, 6000)
        # ball
        frame = self.world.get_latest_frame()
        if frame and frame.ball:
            state.ball_position = (frame.ball.x, frame.ball.y)
            state.ball_timestamp = time.time()
        else:
            state.ball_position = None

        # nearest
        if state.ball_position:
            state.nearest_robot = Nearest.robot(state.ball_position, self.robots)

            try:
                ordered = Nearest.robot_ordered(state.ball_position, self.robots.copy())
                state.nearest_order = list(ordered)
            except Exception:
                state.nearest_order = []
        else:
            state.nearest_robot = None
            state.nearest_order = []

        # goalie intercept prediction 
        if state.ball_position:
            hist = []
            frames = self.world.get_last_n_frames(7)
            for f in frames:
                if f.ball:
                    hist.append([f.ball.x, f.ball.y])
            if hist:
                goalie_pos, threat = predict_trajectory(hist, 3, isPostive=self.world.us_positive, feild_size=state.field_size)
                state.goal_threat = bool(threat)
                state.goalie_save_position = goalie_pos
            else:
                state.goal_threat = False
                state.goalie_save_position = None
        else:
            state.goal_threat = False
            state.goalie_save_position = None

    
        if hasattr(self.world, "ref_data"):
            state.gc_command = getattr(self.world.ref_data, "command", None)
            state.gc_stage = getattr(self.world.ref_data, "stage", None)

        return py_trees.common.Status.SUCCESS