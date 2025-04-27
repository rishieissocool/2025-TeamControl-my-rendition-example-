### Game controller Receiver
from TeamControl.Network import Multicast
from TeamControl.SSL.proto2 import ssl_gc_referee_message_pb2
### GC - Recv
class GameControl(Multicast):
    def __init__ (self, port : int=10003)-> None:
        """
        Initialising Multicast Vision SSL Socket

        Args:
            world_model (wm): current world model
            ip (str, optional): ip of Device. Defaults to None -> local. input if other device
            port (int, optional): Port for Game Controller Referee. Defaults to 10003. consult if changing
        """
        decoder :object = ssl_gc_referee_message_pb2.Referee()
        group : str = "224.5.23.1"
        buffer_size : int = 6000
        # group : str = "GC.GlOBAL"
        super().__init__(port=port, group=group, decoder=decoder,buffer_size=buffer_size)

    def listen(self, duration: int = None) :
        ref_msg = super().listen(duration)
        return ref_msg


