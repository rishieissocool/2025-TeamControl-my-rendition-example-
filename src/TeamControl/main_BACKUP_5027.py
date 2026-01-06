from multiprocessing import Process, Queue

from TeamControl.SSL.vision.Process import vision_worker
from TeamControl.SSL.game_controller.fsm import run_gcfsm
from TeamControl.world.model_manager import WorldModelManager
from TeamControl.world.model_runner import wm_runner
<<<<<<< HEAD
=======
# from TeamControl.utils.dummy_process import DummyReader
from TeamControl.utils.follow_ball_dummy import run_follow_ball_dummy
>>>>>>> main
from TeamControl.robot.goalie import run_goalie
from TeamControl.network.proto2 import *
from TeamControl.dispatcher.dispatch import run_dispatcher
from TeamControl.voronoi_planner.run_planner import run_planner
from TeamControl.robot.striker import run_striker
from TeamControl.robot.unittest import run_test_to_goal
from TeamControl.plotter.plot import run_plotter


def main():
    use_sim = True
    is_yellow = True

    # queues
    vision_q = Queue()
    gc_q = Queue()
    dispatch_q = Queue()
    planner_q = Queue()

    # world model
    wm_manager = WorldModelManager()
    wm_manager.start()
    wm = wm_manager.WorldModel()
    wmr = Process(target=wm_runner, args=(wm, vision_q, gc_q))

<<<<<<< HEAD
    # processes
    vision_wkr = Process(target=vision_worker, args=(vision_q, use_sim))
    gc_wkr = Process(target=run_gcfsm, args=(gc_q,))
    dispatch_wkr = Process(target=run_dispatcher, args=(dispatch_q, use_sim, is_yellow))
    planner_wkr = Process(target=run_planner, args=(wm, dispatch_q))
    striker_wkr = Process(target=run_striker, args=(dispatch_q, wm, 0, is_yellow))
    # plot_test = Process(target=run_test_to_goal, args=(wm,))
    plot_test = Process(target=run_plotter, args=(wm,))
=======
    # goalie = Process(target=run_goalie,args=(dispatch_q,wm,0,is_yellow))
    chaser = Process(target=run_follow_ball_dummy,args=(dispatch_q,wm,1,is_yellow))
    # some_other_process2 = Process(target=DummyReader,args=(wm,))'
>>>>>>> main
    
    vision_wkr.start()
    gc_wkr.start()
    wmr.start()
    dispatch_wkr.start()
<<<<<<< HEAD
    # planner_wkr.start()  # enable if you want path planner
    striker_wkr.start()

    plot_test.start()

=======
    chaser.start()
    # planner_wkr.start()
    # some_other_process2.start()
    
>>>>>>> main
    vision_wkr.join()
    gc_wkr.join()
    wmr.join()
    dispatch_wkr.join()
<<<<<<< HEAD
    # planner_wkr.join()
    striker_wkr.join()
    plot_test.join()

=======
    chaser.join()   
    # planner_wkr.join()
    # some_other_process2.join()
>>>>>>> main

if __name__ == "__main__":
    main()
