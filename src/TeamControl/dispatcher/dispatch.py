from multiprocessing import Process, Queue, Event
from TeamControl.utils.Logger import LogSaver
from TeamControl.process_workers.worker import BaseWorker
from TeamControl.network.robot_command import RobotCommand
from TeamControl.network.YamlSender import YamlSender
from TeamControl.network.ssl_sockets import grSimSender
import time
from pathlib import Path

import yaml
try:
    from yaml import CLoader as Loader
except ImportError as e:
    from yaml import Loader


class Dispatcher(BaseWorker):
    def __init__(self,is_running:Event ,logger:LogSaver ):
        super().__init__(is_running,logger)
        path = Path(__file__).resolve()
        self.running_commands = {}

    def setup(self,*args):
        q,use_sim  = args
        self.q = q
        self.use_sim = use_sim
        self.y_sender = YamlSender(send_to_grSim=use_sim) 
        self.announce_initialisation()
        
    # Announce that the dispatcher has been created
    def announce_initialisation(self):
        print("Multi-robot dispatcher initialized!")
        print("Simulation is active :", self.use_sim)
    
    # Main processing loop
    def run(self):
        return super().run()
    
    def step(self,is_running):
        self.check_new_commands()
        self.handle_commands()
        self.check_command_timeout()
        
    def shutdown(self):
        self.reset_all_robots()
        self.handle_commands()
        super().shutdown()
    # Get the next command from the queue and add it
    def check_new_commands(self):
        if not self.q.empty():
            queue_item = self.q.get_nowait()
            command, runtime = queue_item # this requires a command and runtime
            self.add(command, runtime)
        else:
            time.sleep(0.005)

    # Add a new command to the running commands and replace exisiting commands for the robot with the same ID
    def add(self, command, run_time):
        robot_id = command.robot_id
        isYellow = command.isYellow
        self.running_commands[robot_id] = {"isYellow": isYellow,"command": command, "runtime": run_time, "start_time": time.time()}
        print(f"[{robot_id=},{isYellow=}] New command added for {run_time}s , command: {command}")
        
    # Check if any commands have expired
    def check_command_timeout(self):
        expired_commands = []
        
        for robot_id, packet in self.running_commands.items():
            elapsed_time = time.time() - packet["start_time"]
            
            if elapsed_time >= packet["runtime"]:
                print(f"[Robot {robot_id}] Command expired after {elapsed_time:.2f}s")
                expired_commands.append(robot_id)

        for robot_id in expired_commands:
            self.reset_command(robot_id)

    # Set a do nothing command for the specified robot
    def reset_command(self, robot_id):
        isYellow = self.running_commands[robot_id]["isYellow"]
        reset_command = RobotCommand(robot_id=robot_id, vx=0, vy=0, w=0, kick=0, dribble=0,isYellow=isYellow)
        print(f"[Robot {robot_id}] Reset to idle command")
        
        self.running_commands[robot_id] = {"isYellow" : isYellow, "command": reset_command, "runtime": 9999999, "start_time": time.time()}

    def reset_all_robots(self):
        for i in self.running_commands:
            robot_id = self.running_commands[i]
            self.reset_command(robot_id=robot_id)
            
                
    # Handle all active commands for all robots
    def handle_commands(self):
        for robot_id, packet in self.running_commands.items():
            command = packet["command"]
            self.send_command(command)
            
    def send_command(self,command:RobotCommand):
        # this handles how you'd use different senders to send a command.
        self.y_sender.send_command(command)
        if self.send_to_grSim:
            self.y_sender.send_grSim_command(command)
            
# def run_dispatcher(is_running,q,use_sim,is_yellow):
#     d = dispatch(q=q,use_sim=use_sim,is_yellow=is_yellow)
#     d.process_q(is_running)