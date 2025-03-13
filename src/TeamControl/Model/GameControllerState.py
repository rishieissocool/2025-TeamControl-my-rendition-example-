"""
Author : Emma Tsang
This file parse in Referee Messages. 
"""

from dataclasses import dataclass
import json
from TeamControl.Model.GameState import *
from TeamControl.Model.world import World
from multiprocessing import Queue

import logging
log = logging.getLogger()
log.setLevel(logging.INFO)


class GC_Processor():
    def __init__(self,states:list ):
        self._current_stage : Stage= None
        self.last_gc_stage_transition = None
        self.states : list= states
        self.us_yellow : bool= None ## assuming that we are yellow until it is changed
        self.us_positive : bool= None
        self.team_info : TeamInfo= None
        self.command : GameControllerCommand= None
        self.next_command : GameControllerCommand= None
        self._current_event : GameEventType= None
        self.proposed_event : GameEventProposalGroup= None
        
    def add_state(self,state:State):
        # if this is not State class, kill program
        if not isinstance(state,State):
            logging.error("Require instance of State Class from GameState.py")
            exit(0)
        self.states.append(state)
        if len(self.states) > 5:
            # get rid of first
            self.states.pop(0)
    
    def get_state(self,num:int) -> State:
        if len(self.states) > 0 :
            # read the wanted Num state (reverse) 
            state = self.states[-num]  # -1 = newest
            return state
    
    def update(self,state: State):
        self.add_state(state)
        
        self._compare_stage(state.stage)
        self._compare_us_yellow_positive(state)
        self._get_ourTeam_message(state)
        self._get_command(state.command,state.nextCommand)
        self._get_event(state.gameEvents,state.gameEventProposal)
        
            
    def _compare_stage(self,stage):
        if self._current_stage != stage:
            self._current_stage = stage
            log.info(f"New Stage : {self._current_stage}")
    
    def _compare_us_yellow_positive(self,state):
        if state.yellow["name"] == "TurtleRabbit" and self.us_yellow is not True:
            self.us_yellow = True
            log.info(f"Updated OurTeam to : isYellow={self.us_yellow}")

        elif state.blue["name"] == "TurtleRabbit"and self.us_yellow is not False:
            self.us_yellow = False
            log.info(f"Updated OurTeam to : isYellow={self.us_yellow}")
        
        new_us_positive = state.blueTeamOnPositiveHalf
        if self.us_yellow is True and state.blueTeamOnPositiveHalf is not None:
            new_us_positive = not(state.blueTeamOnPositiveHalf)
        elif self.us_yellow is False and state.blueTeamOnPositiveHalf is not None:
            new_us_positive = state.blueTeamOnPositiveHalf
        if self.us_positive != new_us_positive:
            self.us_positive = new_us_positive
            log.info(f"Updated OurTeam to : isPositive={self.us_positive}")
    
    def _get_ourTeam_message(self,state):
        if self.us_yellow:
            team_info = state.yellow
        elif not(self.us_yellow):
            team_info = state.blue
            
        if self.team_info != team_info:
            self.team_info = team_info
            log.info(f"TeamInfo Updated{self.team_info}")
    
    def _get_command(self,command,next_command):
        if command is not None and self.command != command: 
            self.command = command
            log.info(f"New Command : {command}")
        if next_command is not None:
            self.next_command = next_command
            log.info(f"The next command is : {next_command}")

    def _get_event(self, event:GameEventType,event_proposal: GameEventProposalGroup):
        if event is not None and self._current_event != event:
            self._current_event = event
        if event_proposal is not None and self.proposed_event != event_proposal:
            self.proposed_event = event_proposal
            

## To begin : 
if __name__ == '__main__':
    from TeamControl.Model.world import World
    from TeamControl.Network.ssl_networking import GameControl, vision, grSimVision
        
    logging.basicConfig(level=logging.INFO)

    isYellow = False
    states = list()
    gc = GC_Processor(states)
    referee_l = GameControl()
    state = referee_l.listen()
    gc.update(state)
    
    world = World(isYellow,isYellow)
    vision_l = vision(world)
    while True:
        state = referee_l.listen()
        gc.update(state)