from TeamControl.utils.goal_trajectory import predict_trajectory, goal_intersection
from . import velocity_est
import math as m 
# Assumptions 
history = []

# Assume that this function is only used for intersection with goal line only
# t = d/v
def time_to_intercept(ball_pos, ball_vel, target):
    _, direction_info, trajectory_y_at_goal_line,_ = predict_trajectory(history = history,
                                                           num_samples = 10,)
    
    intersects_line, intersection_point = goal_intersection(trajectory_y_at_goal_line)
    
    if ball_vel == 0 or direction_info == "Moving away from the goal" or intersects_line == False:
        return None
    
    # Euclidean Distance
    dist = m.sqrt(m.exp(ball_pos[0] ** 2 - intersection_point[0] ** 2) + m.exp(ball_pos[1] - intersection_point[1]))
    
    # Speed (Velocity magnitude)
    
    vx, vy = velocity_est(ball_hist = history)
    v = m.sqrt(vx**2 + vy**2)

    return dist/v


