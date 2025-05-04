from TeamControl.robot_behaviour.Movement import *

r = RobotMovement
Fp = Follow_path()
def get_path_point_test():
    path = ([2, 2], [3, 4], [4, 4], [5, 5]) # you get a path 
    # path = ([1,1])
    robot_pos = [1, 1]
    Fp.update_path(path) # update the path into a class 
    target = Fp.get_point(robot_pos) #then you can call the function to get a traget
    #^ idea just set a path to eatch robot which we can update when we want 
    
    
    print(target)




if __name__ == "__main__":
    get_path_point_test()
