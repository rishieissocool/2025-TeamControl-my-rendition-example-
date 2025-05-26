from multiprocessing import Queue,Process
from TeamControl.SSL.vision.field import GeometryData
from TeamControl.SSL.vision.frame import Frame
from TeamControl.world.model import WorldModel

def wm_runner(wm:WorldModel,vision_q:Queue,gc_q:Queue,interval:int=5):
        count = 0
        while True:
            try:
                if not vision_q.empty():
                    item = vision_q.get_nowait()
                    if isinstance(item,Frame):
                        wm.add_new_frame(item)
                        count += 1
                        if count >= interval:
                            wm.detection_updated = True
                            print(wm.get_latest_frame())
                            count = 0 
                            wm.detection_updated = False
                    elif isinstance(item,GeometryData):
                        wm.update_geometry = item
                        
                # if not self.gc_q.empty():
                #     new_info = self.gc_q.get_nowait()
                #     self.update_game_data(new_info)
                
            except Exception as e:
                print("ERROR", e)