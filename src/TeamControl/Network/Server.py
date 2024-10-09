# from TeamControl.Network.Robot import *
from TeamControl.Network.robotserver import *
from TeamControl.Network.Receiver import *   
from TeamControl.Network.Sender import *

c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)

class Server():
    """Server1 : 
    Test Server on Robot (works with robot-client-2)
    Procedures : (by theory)
    when initiated, the server will first setup sockets for main receiver and broadcast1
    then the broadcast1 will constantly broadcast it's main receiver address
    once a robot sends it's receiving address to the main receiver, 
    The server will asks for user input for id of robot
    Afterwards, the server will generate a sender and receiver channel to that robot(TODO)
    Then a robotclient class will be created to store all relevant data (TODO)

    Since it is still in development process : 
    Currently this only have robot_1_sender and robot_1_receiver implemented. More features will be added.

    TODO : 
        1. Add in multiprocessing or Asyncio to separate broadcast and main receiver from the rest

    Attributes : 
        main_receiver (robotReceiver): server's main receiveing channel.
        broadcaster1 (Broadcast) : server's main broadcast. used for broadcasting main_recving addr for robot registration 
        world_model (wm): the worldmodel of this server. it is auto generated.
        vision_receiver (world(Multicast)): vision world receiver, can be grsim or ssl-visiion.
    """
    def __init__(self, isYellow:bool,is_grSim :bool=False, max_robots:int=6) -> None:
        """Initiating instance
        Arg: 
            is_grSim(bool,optional): Are you using grSim? Defaults to False.
        """
        self.main_receiver:robotReceiver =  robotReceiver()
        self.broadcaster1:Broadcast = Broadcast() #initialising
        # self.broadcaster2:Broadcast = Broadcast()
        self.robots = robots(max_robots)
        self.world_model = wm(isYellow=isYellow)
        if is_grSim: # are you using grSim world data
            self.is_grSim:bool = True
            self.vision_receiver:grSimVision = grSimVision(self.world_model)
        else:
            self.is_grSim:bool = False
            self.vision_receiver:vision = vision(self.world_model)
        
        self.gc_receiver:GameControl = GameControl(self.world_model)
        self.list_action:list = list()
        self.Look4Robots()
        
        
    def Look4Robots(self) -> None:   
        """initialise server
            Broadcasts server's own addr and looks for robots
            Adds gives robot individual channel if found.
            gives robot an id via user input

        Params:
            main_addr(bytes):server's main receiving addr in bytes to be broadcasted
            robot_recv_addr(str): Robot's message (it's own receiving address) 
            robot_id(int): user input-ed robot id
            msg(str) : message to be sent
        """
        main_addr: bytes = bytes(self.main_receiver.get_addr().encode('utf-8'))
        logging.info("Now looking for robots")

        while self.robots.missing_robot : 
            # broadcasting main receiving address
            self.broadcaster1.send(main_addr,duration=0.2)
            # Receiver listens 0.2 second
            robot_receiver_address:str= self.main_receiver.listen(0.2)
            if robot_receiver_address is not None: 
                self.robots.register(robot_receiver_address)
        logging.info("all robots found")
                
        # robot channels are now set 
    
    # def queue_action(self,action:Action):
    #     self.list_action.append(action)
    
    def send_action(self,list_of_action:list): 
        self.robots.send(list_of_action)
        
    def run(self)-> None:
        """Run function of server
            This is the operation of the server.
            Currently only focuses on go_To_Target function. *Needs work*

        Params:
            updated(bool): whether the current frame has been updated.
            ball_pos(tuple[float, float]): position x, y of ball
            action (Action): action to be sent
        """
        from TeamControl.RobotBehaviour.goToTarget import go_To_Target
        from TeamControl.Model.transform_cords import world2robot
        robot_id = 1
        while True:
            # print(self.vision_receiver)
            updated= self.vision_receiver.listen()
            list_action = list() 
            
            # print(updated)
            if updated:
                logging.info("hi")
                ball_pos = self.world_model.get_ball()
                if ball_pos is not None:
                    logging.info(ball_pos)
                    target = world2robot(self.world_model.get_our_robot(robot_id), ball_pos)
                    action = go_To_Target(target)
                    print(action)
                    list_action.append(action)
                    print("action sent")
                    self.send_action(list_action)        

            

    
    
if __name__ == "__main__":
    
    server = Server(isYellow=True,is_grSim=True,max_robots=3)
    # server.run()