from TeamControl.Network.receiver import Multicast
from TeamControl.SSL.proto2 import ssl_vision_wrapper_pb2,ssl_vision_detection_tracked_pb2
from TeamControl.SSL.Vision.world import World as wm
import logging

# Classes of Vision Wolrd Receivers
class Vision(Multicast):
    """ Vision SSL multicast receiver
        world vision SSL  mulitcast listener
    Args:
        Multicast (Class): base Class
    """
    def __init__(self, world_model: wm, port : int=10005) -> None:
        """
        Initialising Multicast Vision SSL Socket

        Args:
            world_model (wm): current world model
            port (int, optional): Port for Vision World multicast. Defaults to 10005. change accordingly if needed
        """
        if not isinstance(world_model, wm) :
            raise ValueError('Wrong world_model input, *world_model has to be a Model object from TeamControl.World.model.')
        decoder :object = ssl_vision_wrapper_pb2.SSL_WrapperPacket()
        group : str = "224.5.23.2"
        buffer_size : int = 6000
        # group = "VISIONSSL.GLOBAL"
        super().__init__(port=port,group=group,decoder=decoder,buffer_size=buffer_size)
        self.world_model = world_model
   
    def listen(self) -> bool:
        new_data = super().listen()
        is_updated:bool = self.world_model.update(new_data)
        logging.info(f"World Model has been updated")
        return is_updated
    
class VisionTracker(Multicast):
    """
    For Tracked Packets

    Args:
        Multicast: the recv socket
    """
    def __init__(self, port, group, decoder, buffer_size = 6000, timeout = 1):
        port = 1234
        decoder = ssl_vision_detection_tracked_pb2.TrackerWrapperPacket()
        group : str = "224.5.23.2"
        buffer_size : int = 6000
        super().__init__(port, group, decoder, buffer_size, timeout)
    