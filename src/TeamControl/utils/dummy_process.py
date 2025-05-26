from TeamControl.world.model import WorldModel
import time

class DummyReader():
    def __init__(self, wm:WorldModel):
        self.wm:WorldModel = wm
        self.last_version = 0
        self.loop()
        
    def loop(self):
        last_update = time.time()
        while True:
            current_version = self.wm.get_version()
            # print(current_version)
            if current_version > self.last_version:
                print(f"{time.time() - last_update}, {len(self.wm.get_last_n_frames(10))}")
                last_update = time.time()
                self.last_version = current_version
                