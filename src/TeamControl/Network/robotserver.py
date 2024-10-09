"""
    This class controls robot connections and communications
"""
import logging
import time
import numpy as np
import ast 
import numpy.typing as npt
import multiprocessing as mp

from multiprocessing import Queue

from TeamControl.Network.Robot import Robot
from TeamControl.shared.Action import Action

log = logging.INFO
c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)

class robots():
    def __init__(self, num_robots:int= 6):
        """
        Purpose: robots
        """
        self.missing_robot = True
        self.action_list:Queue = None
        self.num_robots = num_robots
        self.client_list: list = list()

### supplement function ### 
    def get_addr(self,action:Action):
        if not isinstance(action,Action):
            raise TypeError("Please put Action object only !")
        # gets robot id
        robot_id:int = action.robot_id
        if self.__contains__(robot_id):
            robot = self.__getitem__(robot_id)
            destination = robot.addr
            logging.info(f"Robot:{robot_id} is found @ {destination=}")
            return destination
        else : 
            logging.warning(f"{robot_id=} not found.")
            return None
        

    def check_max(self):
        """check_max checks if we have the max number of robots connected
        """
        if len(self) == self.num_robots:
            logging.info("All robots Found")
            self.missing_robot = False # Terminates main server process
            return False
        elif len(self) > self.num_robots:
            logging.info(f"Warning : there are {len(self)} robots, maximum set : {self.num_robots}")
            self.missing_robot = False
            return False

        else:
            logging.info("looking for robots")
            self.missing_robot = True
            return True

    
    def update_max(self, max:int):
        self.num_robots:int= max 
    
    def update_robot(self, message: str):
        robot_id = int(message[0])
        addr = message[1]
        if len(message)>2:
            info = message[2]
        if isinstance(addr,str):
            addr = ast.literal_eval(addr)

        if addr in self and robot_id in self:
            robot:Robot = self.__getitem__(addr)
            robot.update_last_active() # updates to current time
            logging.info(f"{TIME} RECEIVED {info=}")
           # robot.last_action = info #something
        elif addr in self and not robot_id in self :
            robot:Robot = self.__getitem__(addr)
            robot.id = robot_id
            logging.warning(f"{TIME} Robot with address @ {addr} now been updated from {robot.id} to {robot_id}")
        # elif robot_id in self and not addr in self:
        #     robot:Robot = self.__getitem__(robot_id)
        #     logging.warning(f"{TIME} Robot with ID : {robot_id} already exists @ {robot.addr}. Aborting connection from {addr}")
        elif robot_id not in self and addr not in self:
            self.add_client(robot_id,addr)
            logging.warning(f"{TIME} Robot with ID : {robot_id} @{addr} has now been added")
        

    # def register(self,robot_id:int,addr:str)-> Action:
    #     reg_completed = False
    #     robot_id, address = message.split(" ")
    #     while not reg_completed: 
    #         logging.info(f"{TIME} Robot {robot_id} : Requesting Connection @ {address}")
    #         logging.info("Currently Active : ", str(self))
    #         if self.__contains__(address):
    #             robot = self.__getitem__(address)
    #             logging.info(f"{robot.addr} found with id {robot.id} has now been updated to {robot_id}")
    #             robot.id = robot_id
    #             reg_completed = True
    #             # sends message to reconnect
    #             logging.info(f"robot {robot.id} has been reconnected")
    #         else:
    #             # robot_id = int(input("Please type robot id"))
    #             reg_completed = self.add_client(robot_id,address)
    #             logging.info(f"New robbot {robot_id} has been connected @{address}")
                    
        
    #         action:Action = Action(robot.id)
    #         self.check_max()
    #         return action
                    
    def add_client(self, id: int, robot_receiving_addr: tuple[str,int]) -> bool:
        '''add 
            adds a new Robot Client Connection into the server
        Args:
            id (int): unique id
            robot_client_addr str: ip_addr and port to communicate with robot
        Params : 
            ip_addr (str) : string of robot ipv4 address
            port (int) : receiving port
            robot (Robot) : the robot that needs to be change or added to port
        '''   
        # remove_robot_with_id = False
        # remove_robot_with_addr = False

        ip_addr,port = robot_receiving_addr
            
        # if ip_addr in self:
        #     logging.warning(f'robot with id: {self.__getitem__(ip_addr).id} @ {ip_addr} exists!\n Would you like to replace it ? [y/n]')
        #     ans = input()
        #     if ans == "y":
        #         remove_robot_with_addr = True
        #     else:
        #         print("Cancelled.")
        #         return True
            
        # if id in self:
        #     logging.warning(f'robot with id: {id} exists @{self.__getitem__(id).addr}!\n Would you like to replace it ? [y/n]')
        #     ans = input()
        #     if ans == "y":
        #         remove_robot_with_id = True
        #     else:
        #         print("Cancelled. Please try with another ID")
        #         return False
        
        # if remove_robot_with_addr:
        #     self.remove_client(ip_addr)
        # if remove_robot_with_id:
        #     self.remove_client(id)
            
        # adds new robot
        robot = Robot(id, ip_addr,port)
        self.client_list.append(robot)
        self.client_list.sort()
        return True


    def remove_client(self, item: int|str) -> None:
        '''
            remove a robot-client
        @args:
            item (int|str) id or ip_addr of robot-client to be removed
        '''
        robot = self[item]
        try:
            self.client_list.remove(robot)
            logging.info(f"REMOVED {str(robot)}")
        except Exception as e:
            logging.critical(e)
        del robot
        
    
    def __len__(self) -> int:
        return len(self.client_list)
    
    def __str__(self) -> str:
        x: str = f"num_robots: {len(self)}\n"
        x += "".join([f"Id: {x.id} @ {x.addr}\n" for x in self.client_list])
        return x
    
        
    def __getitem__(self, item: int|str) -> Robot|None:
        if isinstance(item, int):
            try:
                robot:Robot = [x for x in self.client_list if x.id == item][0]
                return robot
            except IndexError as e:
            #    print(f"__getitem__(): {e}")
                pass
        if isinstance(item,str):
            try:
                robot: Robot = [x for x in self.client_list if x.addr == item][0]
                return robot
            except IndexError as e: 
            #    print(f"__getitem__(): {e}")
                pass
        # otherwise return none
        return None

    def __contains__(self, item: int | Robot | str) -> bool:
        '''
            for "in: reserved keyword
            if `id` or `addr` is already in use
            return True
        '''
        if isinstance(item, int):
            robot_id = item
            if robot_id in [x.id for x in self.client_list]:
                return True        
        if isinstance(item, Robot):
            if item in self.client_list:
                return True
            
        if isinstance(item, str):
            ip_addr = item
            if ip_addr in [x.addr for x in self.client_list]:
                return True

        return False


if __name__ == "__main__":
    server = robots(num_robots=6)
    server.add_client(0,"('127.0.0.1',12341)")    
    server.add_client(1,"('127.0.0.1',12341)")    
    server.add_client(1,"('127.0.0.2',12342)")    
    server.add_client(2,"('127.0.0.3',12343)")    
    server.add_client(3,"('127.0.0.4',12344)")    
    server.add_client(4,"('127.0.0.5',12345)")    
    server.add_client(5,"('127.0.0.6',12346)") 
    
    server.add_client(7,"('127.0.0.6',12346)") # gives you a prompt for update
    server.add_client(2,"('127.0.0.2',12346)") # ignores this  
    server.add_client(4,"('127.0.0.8',12346)") # ignores this  

    server.remove_client(0)
    server.add_client(0,"('127.0.0.7',12346)") # should add this.
    server.add_client(11,"('127.0.0.9',12346)") # should add this. # this may give u a warning 
    
    server.check_max()
    print(server)
    
    print(f"{server.missing_robot=}")