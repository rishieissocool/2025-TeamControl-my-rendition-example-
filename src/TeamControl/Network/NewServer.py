"""
This script is an archive
"""

import logging
import time
import numpy as np
import ast 
import numpy.typing as npt
import multiprocessing as mp

from multiprocessing import Queue,freeze_support,Process,Manager

from TeamControl.Network.Sender import robotSender,Broadcast
from TeamControl.Network.Receiver import robotReceiver,vision,grSimVision,GameControl
from TeamControl.Network.robotserver import robots
from TeamControl.Coms.Action import RobotAction as Action
from TeamControl.Model.world import World as wm
# from TeamControl.Model.game3 import test
# from TeamControl.Model.game2 import tc
from TeamControl.Model.GameState import GameControllerCommand


"""
This class controls server main operation. Utilises multiprocessing.
*Please make sure that this does not have input
"""
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)



# main functions
# def broadcast(namespace):
#     broadcaster = Broadcast()
#     logging.info(f"Broadcast initialise : {broadcaster}")
#     while namespace.looking4robots is True: #forever looping *this will be updated from other process
#         if namespace.address is not None:
#             log.debug(f"broadcasting receiver address: {namespace.address} ")
#             broadcaster.send(namespace.address) 
#             time.sleep(0.02)  

# def recv(namespace):
#     recv_sock = robotReceiver()
#     print(f"RECV : {recv_sock} ACTIVE")
#     # updates address for sending
#     namespace.address = bytes(recv_sock.get_addr().encode('utf-8'))
#     while True:
#         data = recv_sock.listen()
#         message = data.split(':')
#         print(f"RECEIVED : {message[0]} {message[1]}")
#         namespace.robots.update_robot(message)
#         log.info(f"all robots found? : {namespace.robots.check_max()=}")
#         if namespace.robots.check_max():
#             namespace.looking4robots = False
#             print(f"now has set {namespace.looking4robots=}")
#         print(namespace.robots) #prints all active in robotserver
#         log.debug(f"Robot {message[0]} has been updated {message=}")



def send(namespace,action_queue:Queue):
    send_sock = robotSender(port=50514)
    destination = {
        1: ("192.168.1.152",50514),
        2: ("192.168.1.153",50514),
        3: ("192.168.1.152",50514),
        4: ("192.168.1.152",50514),
        5: ("192.168.1.152",50514),
        6: ("192.168.1.152",50514),
    }
    print(f"SENDER : {send_sock} ACTIVE")
    while True:
        # r = namespace.robots
        # if action_list is not empty:
        if not action_queue.empty():
            # gets first action
            action:Action = action_queue.get()
            # gets destination from id
            robot_id = action.robot_id
            dest= destination[robot_id]
            # print("destination",destination)
            # encodes action
            msg:str = action.encode()
            # sends action
            if destination is not None:
                send_sock.send(msg,destination=destination)
                # log.debug(f"SENT {action=} @ {destination}")
                log.info(f"SENT {action=} @ {destination}")

def vision_recv(namespace):
    vision_sock = vision(namespace.wm)
    # vision_sock = grSimVision(namespace.wm)
    while True:
        updated = vision_sock.listen()
        if updated:
            namespace.is_world_model_updated = True
            # print(vision_sock.world_model)
            # log.debug(f"vision is updated: {updated}")
            namespace.wm = vision_sock.world_model
            # print("world model has been updated")
            # print("world model is now updated")
        else : 
            namespace.is_world_model_updated = False
            # print("world model is still updating")
            #gets world model from pipe ? 
            # stores into share space world model list
            #world_model = vision_sock.world_model

def game_recv(states_queue:Queue):
    game_sock = GameControl()
    while True:
        new_state = game_sock.listen()            
        states_queue.put(new_state)
        log.debug(f"states has been added")

def main_process(namespace,action_queue: Queue,states_queue: Queue):
    # player = test(namespace,action_queue,states_queue)
    player = tc(namespace,states_queue,action_queue)
   
    while True:
       
        if namespace.is_world_model_updated is True:
            world_model = namespace.wm
            player.update_world(world_model)
        
        if not states_queue.empty():
            new_state = states_queue.get()
            player.stage_transition_handler(new_state.stage)
            player._tc_gc_state_controller.log_gc_cmd_transition(new_state)
            print(new_state)
            
        cmd_func = player._tc_gc_state_controller.gc_callable_cmd
        log.warn(f'{cmd_func=}')
        if not cmd_func is None:
            cmd_func()
        
        action_queue = player._tc_gc_state_controller.send_to_robot_q
        




    # player = tc(namespace)
# def test(action_queue):
#     """ this test action putting into the queue
#         puts an action into the queue /1 second
#     """
#     while True:
#         action = Action(1,1,1,1,1)
#         action_queue.put(action)  
#         time.sleep(1)  

if __name__ == "__main__":
    freeze_support()
    manager = mp.Manager()
    namespace = manager.Namespace()

    
    namespace.is_world_model_updated = False
    namespace.wm = wm(isPositive=True,isYellow=True,max_frames=5,max_cameras=1)
    # namespace.robots =robots(1)
    # namespace.looking4robots = True
    # namespace.address = None
    
    states_queue: Queue = Queue()
    action_queue:Queue = Queue() 
    
    # broadcast_process = mp.Process(target=broadcast, args=(namespace,))
    # main_recv = mp.Process(target=recv, args=(namespace,))
    vis = mp.Process(target=vision_recv, args=(namespace,))
    game = mp.Process(target=game_recv, args=(states_queue,))
    main_send = mp.Process(target=send, args=(namespace,action_queue,))
    team_operations = mp.Process(target=main_process,args=(namespace,action_queue,states_queue))
    # other_process = mp.Process(target=other_process)

    # broadcast_process.start()
    # main_recv.start()
    vis.start()
    game.start()
    main_send.start()
    team_operations.start()
    # test_operation.start()

    # broadcast_process.join()
    # main_recv.join()
    vis.join()
    game.join()
    main_send.join()
    team_operations.join()
    # test_operation.join()
