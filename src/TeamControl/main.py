from multiprocessing import Process, Queue,Event
from TeamControl.SSL.vision.Process import vision_worker
# from TeamControl.SSL.game_controller.compare import game_controller_worker
from TeamControl.SSL.game_controller.fsm import run_gcfsm
from TeamControl.world.model_manager import WorldModelManager
from TeamControl.world.model_runner import wm_runner
from TeamControl.utils.dummy_process import DummyReader
from TeamControl.utils.remote_control_process import RCProcess,run_rc_process
from TeamControl.robot.goalie import run_goalie

# in multiprocessing this can only be a simple process

def main():
    use_sim = True
    vision_q = Queue()
    gc_q = Queue()
    # robot_feedback_q = Queue()
    
    # inputs
    vision_wkr = Process(target=vision_worker, args=(vision_q,use_sim,))
    gc_wkr = Process(target=run_gcfsm, args=(gc_q,))
    
    # world model
    wm_manager = WorldModelManager()
    wm_manager.start()
    wm = wm_manager.WorldModel()
    wmr = Process(target=wm_runner, args=(wm,vision_q,gc_q,))
    
    goalie = Process(target=run_goalie,args=(wm,5))
    # some_other_process2 = Process(target=DummyReader,args=(wm,))
    vision_wkr.start()
    gc_wkr.start()
    wmr.start()
    goalie.start()
    # some_other_process2.start()
    
    vision_wkr.join()
    gc_wkr.join()
    wmr.join()
    goalie.join()
    # some_other_process2.join()

if __name__ == "__main__":
    main()