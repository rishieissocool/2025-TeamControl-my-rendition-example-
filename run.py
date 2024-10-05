#! /usr/bin/env python3

import logging
import time
import multiprocessing
from multiprocessing import freeze_support
from TeamControl.Model.Stage import concrete_tc_
from TeamControl.SimpleNetwork.SimpleSender import DummyUDPServer

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(ch)

from TeamControl.Network.Receiver import robotReceiver,vision,grSimVision,GameControl
from TeamControl.Model.world import World
from TeamControl.Model.GameState import State

def vision_recv(namespace, vision_ssl_recv_event):
    vision_sock = vision(namespace.world_model)
    # vision_sock = grSimVision(namespace.wm)
    while True:
        updated = vision_sock.listen()
        # log.critical(updated)
        if updated:
            namespace.is_world_model_updated = True
            # print(vision_sock.world_model)
            # log.debug(f"vision is updated: {updated}")
            namespace.world_model = vision_sock.world_model
            vision_ssl_recv_event.set()
            # log.warn(namespace.world_model)
        else : 
            namespace.is_world_model_updated = False

def gc_recv(new_state_q, new_state_recv_event):
    gc_sock = GameControl()
    while True:
        new_state = gc_sock.listen()
        new_state_q.put(new_state)
        new_state_recv_event.clear()
        
def new_game(namespace, new_state_q, action_send_q, vision_ssl_recv_event, new_state_recv_event):
    new_tc = concrete_tc_(namespace, new_state_q, action_send_q)
    while True:
        # vision_ssl_recv_event.wait()
        # new_state_recv_event.wait()
        new_tc.world_model = namespace.world_model
        new_tc.run()
        time.sleep(0.1)
        # vision_ssl_recv_event.clear()
        # new_state_recv_event.clear()

def dummy_action_consumer(send_to_robot_q):
    new_server = DummyUDPServer(send_to_robot_q)
    while True:
        if not send_to_robot_q.empty():
            new_server.send()

        time.sleep(.1)


if __name__ == '__main__':
    freeze_support()

    manager = multiprocessing.Manager()
    namespace = manager.Namespace()

    world_model = World(isYellow=True, isPositive=True, max_cameras=1)
    namespace.world_model = world_model

    vision_ssl_recv_event = multiprocessing.Event()
    vision_ssl_recv = multiprocessing.Process(target=vision_recv, args=(namespace,vision_ssl_recv_event), name="vision_ssl_reciever")

    new_state_q = multiprocessing.Queue()
    state_gc_recv_event = multiprocessing.Event()
    gc_recv_process = multiprocessing.Process(target=gc_recv, args=(new_state_q, state_gc_recv_event), name="game_control_reciever")

    new_action_send_event = multiprocessing.Event()
    action_send_q = multiprocessing.Queue()
    team_controller = multiprocessing.Process(target=new_game, args=(namespace, new_state_q, action_send_q, vision_ssl_recv_event, state_gc_recv_event), name="team_control")

    send_to_robot = multiprocessing.Process(target=dummy_action_consumer, args=(action_send_q,), name="send_to_robot")

    vision_ssl_recv.start()
    gc_recv_process.start()
    team_controller.start()
    send_to_robot.start()

    vision_ssl_recv.join()
    gc_recv_process.join()
    team_controller.join()
    send_to_robot.join()

