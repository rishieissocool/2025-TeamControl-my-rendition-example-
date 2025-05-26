from multiprocessing import Process, Queue
from TeamControl.SSL.vision.Process import VisionProcess
from TeamControl.SSL.game_control.Processing import Processing
from TeamControl.world.model import WorldModel

# in multiprocessing this can only be a simple process

def main():
    use_sim = True
    vision_q = Queue()
    gc_q = Queue()
    vision_wkr = Process(target=VisionProcess, args=(vision_q,use_sim,))
    wm = Process(target=WorldModel, args=(vision_q,gc_q,5))
    
    vision_wkr.start()
    wm.start()

if __name__ == "__main__":
    main()