from TeamControl.network.receiver import Multicast
from TeamControl.SSL.proto2 import ssl_vision_wrapper_pb2,ssl_vision_detection_tracked_pb2
import logging

# Classes of Vision Wolrd Receivers
class Vision(Multicast):
    """ Vision SSL multicast receiver
        world vision SSL  mulitcast listener
    Args:
        Multicast (Class): base Class
    """
    def __init__(self,port : int=10006) -> None:
        """
        Initialising Multicast Vision SSL Socket

        Args:
            world_model (wm): current world model
            port (int, optional): Port for Vision World multicast. Defaults to 10005. change accordingly if needed
        """
        decoder :object = ssl_vision_wrapper_pb2.SSL_WrapperPacket()
        group : str = "224.5.23.2"
        buffer_size : int = 6000
        # group = "VISIONSSL.GLOBAL"
        super().__init__(port=port,group=group,decoder=decoder,buffer_size=buffer_size)
   
    def listen(self) -> bool:
        vision_data,addr = super().listen()
        return vision_data
            
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
    