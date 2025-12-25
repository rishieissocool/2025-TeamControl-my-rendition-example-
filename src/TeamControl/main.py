from TeamControl.SSL.vision.Process import vision_worker
# from TeamControl.SSL.game_controller.compare import game_controller_worker
from TeamControl.SSL.game_controller.fsm import run_gcfsm
from TeamControl.world.model_manager import WorldModelManager
from TeamControl.world.model_runner import wm_runner


from TeamControl.dispatcher.dispatch import run_dispatcher

from TeamControl.voronoi_planner.run_planner import run_planner
# from TeamControl.behaviour_tree.run_bt_process import run_bt_process
# from TeamControl.utils.dummy_process import DummyReader
from TeamControl.utils.follow_ball_dummy import run_follow_ball_dummy
from TeamControl.robot.goalie import run_goalie


# in multiprocessing this can only be a simple process
from multiprocessing import Process, Queue,Event

# use this to catch keyboard interrupt
import sys

import time

def main():
    # add a timer
    start_time = time.time()
    # add a timer
    start_time = time.time()
    use_sim = True
    is_yellow = True
    
    # queues
    vision_q = Queue()
    gc_q = Queue()
    dispatch_q = Queue()
    planner_q = Queue()
    
    # robot_feedback_q = Queue()
    
    # event : System running ? 
    is_running = Event()
    
    # event : System running ? 
    is_running = Event()
    
    # world model
    wm_manager = WorldModelManager()
    wm_manager.start()
    wm = wm_manager.WorldModel()
    wmr = Process(target=wm_runner, args=(is_running,wm,vision_q,gc_q,),daemon=True)
    wmr = Process(target=wm_runner, args=(is_running,wm,vision_q,gc_q,),daemon=True)
    
    # processes
    vision_wkr = Process(target=vision_worker, args=(is_running,vision_q,use_sim,),daemon=True)
    gc_wkr = Process(target=run_gcfsm, args=(is_running,gc_q,),daemon=True)
    dispatch_wkr = Process(target=run_dispatcher, args=(is_running,dispatch_q,use_sim,is_yellow,),daemon=True)
    # planner_wkr = Process(target=run_planner, args=(wm,dispatch_q))

    # goalie = Process(target=run_goalie,args=(dispatch_q,wm,0,is_yellow))
    # chaser = Process(target=run_follow_ball_dummy,args=(dispatch_q,wm,1,is_yellow))
    # some_other_process2 = Process(target=DummyReader,args=(wm,))'
    
    is_running.set()
    is_running.set()
    vision_wkr.start()
    gc_wkr.start()
    wmr.start()
    # goalie.start()
    dispatch_wkr.start()
    # bt.start()
    # chaser.start()
    # planner_wkr.start()
    # some_other_process2.start()

    while is_running.is_set():
        try:

            print("Type 'exit' to quit: ")
            user_input = input()
            if user_input.lower() == 'exit':
                print("Shutdown signal received...")
                is_running.clear()
                break
        except KeyboardInterrupt:
            print("\nShutdown signal received...")
            is_running.clear()
            # sys.exit()


        # Give processes time to see the event change and shut down
        print("Waiting for processes to shut down...")
        time.sleep(1)  # or 2 seconds if needed

    # Then wait for processes
    vision_wkr.join(timeout=5)
    gc_wkr.join(timeout=5)
    wmr.join(timeout=5)
    dispatch_wkr.join(timeout=5)
            
    # bt.join()
    # chaser.join()   
    # goalie.join()

    # planner_wkr.join()
    # some_other_process2.join()
        
        
        
        
if __name__ == "__main__":
    main()