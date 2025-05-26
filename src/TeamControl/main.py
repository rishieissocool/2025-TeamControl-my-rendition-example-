from multiprocessing import Process, Queue
from TeamControl.SSL.vision.Process import VisionProcess
from TeamControl.SSL.game_control.Processing import Processing
from TeamControl.world.model_manager import WorldModelManager
from TeamControl.world.model_runner import wm_runner

# in multiprocessing this can only be a simple process

def main():
    use_sim = True
    vision_q = Queue()
    gc_q = Queue()
    
    wm_manager = WorldModelManager()
    wm_manager.start()
    wm = wm_manager.WorldModel()
    
    
    vision_wkr = Process(target=VisionProcess, args=(vision_q,use_sim,))
    wmr = Process(target=wm_runner, args=(wm,vision_q,gc_q))
    
    vision_wkr.start()
    wmr.start()
    
    vision_wkr.join()
    wmr.join()

if __name__ == "__main__":
    main()