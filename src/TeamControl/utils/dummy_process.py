from TeamControl.world.model import WorldModel
from TeamControl.SSL.vision.frame import Frame
import time

class DummyReader():
    def __init__(self, wm:WorldModel):
        self.wm:WorldModel = wm
        self.last_version = 0
        self.loop()
        
    def loop(self):
        last_update = time.time()
        while True:
            current_version:int = self.wm.get_version()
            # print(current_version)
            if current_version > self.last_version:
                print(f"{time.time() - last_update}, {self.wm.get_latest_frame().frame_number}")
                last_update = time.time()
                self.last_version = current_version
                robot = self.wm.get_yellow_robots(isYellow=False,robot_id=1)
                print(robot)
                