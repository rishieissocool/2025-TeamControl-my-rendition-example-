import time
from TeamControl.Coms.Action import Action
from TeamControl.Network.Receiver import *
from TeamControl.Network.Sender import *
from TeamControl.Model.world import World as wm
from TeamControl.Coms.grSimAction import grSim_Action
from TeamControl.RobotBehaviour import *
import math
import numpy as np
from TeamControl.Formation.relative_position import *

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression



def predict_trajectory(history: list, num_samples, isPostive:bool, feild_size ):
    '''
        This function takes are input a list of ball positions and uses the last num_samples ball positions
        to fit a ball trajectory by applying a linear regression model. We then check whether this
        trajectory intercepts the goal line. If it does we send this information and the interception
        point to the goalie so the goalie can block the ball.

        History example: [{'x': -118.86381, 'y': 1343.0244}, {'x': -118.86381, 'y': 1343.0244}, ...]

        input:
            history: history of the last ball positions
            num_samples: number of samples that should be used to estimate the trajectory
        output:
            the position the the golie depending on the state of the ball 
    '''
    feild_x, feild_y =feild_size
            # PARAMETERS
    #GOALIE_LINE = -FIELD_LENGTH/2 + 200 #mm #On the other side of the field if we are the other team
    if isPostive == True:
        goal_pos = feild_x/2 - 200
    else:
        goal_pos = -feild_x/2 + 200

    goal_width = 2000
    goal_line = goal_pos # the goal line is the x coordinates of the goals line 
    num_samples = 5
    #print(ball_pos)
    ball_pos_x = []
    ball_pos_y = []
    for ball_pos in history:
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
    if True:
        model = LinearRegression()

        model.fit(np.array(last_ball_positions_x).reshape(-1, 1), last_ball_positions_y)

        # Generate trajectory points
        x_values = np.linspace(-feild_x/2, feild_x/2, 20) 

        current_ball_position_x = ball_pos_x[-1]  # Current ball position

        trajectory_y_at_goal_line = model.predict(np.array([goal_line]).reshape(-1, 1))

        intersect_line = -goal_width / 2 <= trajectory_y_at_goal_line <= goal_width/ 2

        # Calculate intersection point if exists

        golie_pos = None

        # defult goal position is the fomation golie position.
    
        golie_pos = (goal_line, round(trajectory_y_at_goal_line.item()))
       
    return golie_pos, intersect_line
    