'''
 World Model - Central Storage and access control
- apply this in multiprocessing or equivalent 
@author - Emma
'''

<<<<<<< HEAD
from multiprocessing import Queue, Manager
=======
from TeamControl.SSL.vision.frame_list import FrameList
from TeamControl.SSL.vision.field import GeometryData,FieldSize
from TeamControl.SSL.vision.frame import Frame
from TeamControl.SSL.game_controller.common import Command,Stage,GameEventType,Team,PacketType, GameState
from TeamControl.SSL.game_controller.Message import RefereeMessage,TeamInfo

from multiprocessing import Queue,Manager
>>>>>>> main
import numpy as np
import numpy.typing as npt
import logging

from TeamControl.SSL.vision.frame_list import FrameList
from TeamControl.SSL.vision.field import GeometryData, FieldSize
from TeamControl.SSL.vision.frame import Frame
from TeamControl.SSL.game_controller.fsm import PacketType, GameState

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class WorldModel:
    """
    World Model aka wm
    Description : 
        ...
    """

    def __init__(
        self,
        update_interval: int = 10,
        history: int = 60,
        use_sim: bool = True,
        us_yellow: bool = True,
        us_positive: bool = True,
    ):
        mgr = Manager()
        self._us_yellow = us_yellow
        self._us_positive = us_positive
        self.count = 0
<<<<<<< HEAD
        self.update_interval: int = update_interval
        self.use_sim: bool = use_sim
        self.frame_list: FrameList[Frame] = FrameList(history=history)
        self.geometry: GeometryData | None = None
        self.field: FieldSize | None = None
        self._version = mgr.Value("i", 0)

    def update_game_data(self, game_data):
        if isinstance(game_data, Command):
=======
        self.update_interval:int = update_interval
        self.use_sim:bool = use_sim 
        self.frame_list:FrameList[Frame] = FrameList(history=history)
        self.geometry:GeometryData = None
        self.field:FieldSize = None
        self._version = mgr.Value('i', 0)  # int counter
    
    def update_game_data(self,game_data):
        if game_data is None:
            return
        if isinstance(game_data,Command):
>>>>>>> main
            self.ref_data.command = game_data

        elif isinstance(game_data, Stage):
            self.ref_data.stage = game_data

        elif isinstance(game_data, tuple):
            if isinstance(game_data[0], TeamInfo):
                self.ref_data.yellow = game_data[0]
                self.ref_data.blue = game_data[1]

    def update_team(self, us_yellow: bool, us_positive: bool):
        self.us_yellow = us_yellow
        self.us_positive = us_positive
        self.robot_active = 6
        self.game_state = GameState.HALTED
        self.blf_location = None

    def add_new_frame(self, frame: Frame):
        self.count += 1
        if self.count >= self.update_interval:
            self._version.value += 1
            self.count = 0
        self.frame_list.append(frame)

    def update_geometry(self, geometry: GeometryData):
        self.geometry = geometry
        self.field = geometry.field
        self.ball_model = geometry.models

<<<<<<< HEAD
    def update_gc_data(self, packet):
        type, data = packet[0], packet[1]
        match type:
=======
    def update_gc_data(self,packet):
        t, data = packet[0],packet[1]
        match t:
>>>>>>> main
            case PacketType.ROBOTS_ACTIVE:
                self.update_robots_active(data)
            case PacketType.NEW_STATE:
                self.update_state(data)
            case PacketType.SWITCH_TEAM:
                self.update_team(data["YELLOW"], data["POSITIVE"])
            case PacketType.BLF_LOCATION:
                self.update_ball_left_field_location(data)
<<<<<<< HEAD
            case _:
                log.exception(f"undefined {type=}, {data=}")
=======
            
            case _: # if the packet type is unknown 
                log.exception(f"undefined Packet - {t}, {data=}")
            
    def update_robots_active(self,new_active) : 
        self.robot_active = new_active
    
    def update_state(self,new_state):
        # when we have a new incoming state, it updates this
        self._state = new_state 
>>>>>>> main

    def update_robots_active(self, new_active):
        self.robot_active = new_active

    def update_state(self, new_state):
        self._state = new_state

    def update_team(self, us_yellow: bool, us_positive: bool):
        self._us_yellow = us_yellow
        self._us_positive = us_positive

    def update_ball_left_field_location(self, location):
        self.blf_location = location

    def get_ball_left_field_location(self):
        return self.blf_location

    def get_current_state(self):
        return self._state

    def us_yellow(self):
        return self._us_yellow

    def us_positive(self):
        return self._us_positive

    # vision
    def get_latest_frame(self):
        return self.frame_list.latest

    def get_last_n_frames(self, n: int):
        return self.frame_list.get_last_n_frames(n)

    def get_version(self):
        return self._version.value

    # high level
    def get_all_in_team_except(self, us: bool, exclude: list[int]):
        isYellow = self._us_yellow if us is True else not self._us_yellow
        frame = self.frame_list.latest

        if isYellow:
            team = frame.robots_yellow
        else:
            team = frame.robots_blue

        if exclude is None or len(exclude) == 0:
            return team

        for e in list(exclude):
            if e in team:
                team.remove(e)
        return team

    # lower level
    def get_yellow_robots(self, isYellow, robot_id=None) -> object | list:
        if isYellow:
            if isinstance(robot_id, int):
                return self.frame_list.latest.robots_yellow[robot_id]
            return self.frame_list.latest.robots_yellow
        else:
            if isinstance(robot_id, int):
                return self.frame_list.latest.robots_blue[robot_id]
            return self.frame_list.latest.robots_blue

    # higher level
    def get_our_robots(self, us=True, robot_id=None) -> object | list:
        frame = self.frame_list.latest
        is_yellow = self._us_yellow if us else not self._us_yellow
        robots = frame.robots_yellow if is_yellow else frame.robots_blue
        return robots[robot_id] if isinstance(robot_id, int) else robots

    def get_active_robots(self):
        return self.robot_active
