import numpy as np
from numpy import pi
from numpy.linalg import inv


def transformation_matrix(p):
    '''
        input:
            p: robot pose (x, y, theta)
        output:
            transformation matrix (rotation and translation)
    '''
    angle = p[2] 
    c = np.cos(angle)
    s = np.sin(angle)

    transformation_matrix = np.array([
        [c, -s, p[0]],
        [s,  c, p[1]],
        [0,  0,    1]
    ])

    return transformation_matrix

def world2robot(robot_position,target_position):
    '''
        input:
            Target_position: position in the world coordinate system (x,y)
            robot_position: robot pose (x, y, theta)
        output:
            t: targeted position in respect to robot coordinate system (x,y)
    '''
    if robot_position is None or target_position is None:
        print(f"Value is None: {robot_position=}, {target_position=}")
        return
    
    trans_matrix = inv(transformation_matrix(robot_position))
    target_position = np.append(target_position, 1) # (x,y,1)

    t = np.dot(trans_matrix, target_position)[:2]

    return t

def robot2world(r, p):
    '''
        input:
            target_coordinates: position in the robot coordinate system (x,y)
            robot_pos: robot pose (x, y, theta)
        output:
            w: position in the robot coordinate system (x,y)
    '''
    trans_matrix = transformation_matrix(p)
    r = np.append(r, 1) # (x,y,1)

    w = np.dot(trans_matrix, r)[:2]

    return w


def example():
    from TeamControl.Model.world import World as wm
    from TeamControl.Network.Sender import grSimSender,robotSender
    from TeamControl.Network.Receiver import grSimVision,vision
    world_model = wm(True,True)
    print("Are you using grSim 1.YES 2.NO")
    isgrSim = int(input())
    if isgrSim==1:
        receiver = grSimVision(world_model)
    else:
        receiver = vision(world_model)
    while True:
        updated= receiver.listen()
        if updated is True :
            # obtain target
            target = world_model.get_ball()
            
            robot_pos = world_model.get_our_robot(1)
            print(f'{robot_pos=}')
            target_pos = (target[0],target[1])
            # print(matrix_pos)
            # print(robot_pos)(Works)
            print(f'{robot_pos[2]=}')
            matrix = world2robot(r=robot_pos, w=target_pos)
            print(f'{matrix=}')


if __name__ == "__main__":
    example()