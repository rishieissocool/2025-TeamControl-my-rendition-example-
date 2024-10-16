from TeamControl.Coms.Action import Action
from TeamControl.Model.world import World
from TeamControl.Model.transform_cords import world2robot
from TeamControl.RobotBehaviour.behaviour import RobotMovement


def go_to_ball(world_model:World,isYellow:bool,robot_id:int):

    # get positions from the world model
    ball_pos = world_model.get_ball() 
    print(f"{ball_pos=}")
    robot_pos = world_model.get_robot(isYellow=isYellow,robot_id=robot_id)

    # calculate the target position relative to the robot
    pos_relative_to_robot = world2robot(robot_position=robot_pos, target_position=ball_pos)

    # cross check target with path planner
    ## To be implemented . . . 


    # generate the velocity to reach the target 
    vx,vy = RobotMovement.go_To_Target(target_pos=pos_relative_to_robot)
    w = RobotMovement.turn_to_target(pos_relative_to_robot,speed=2)
    
    return Action(robot_id=robot_id,vx=vx,vy=vy,w=w)