""" Game.py 
Stores only the field of ref message we need
"""
from TeamControl.Model.GameState import *
import enum
import typing
from typing import Optional, List, Union
import time

class Point():
    def __init__(self,point):
        # required
       self.x = float(point.x)
       self.y = float(point.y)


class GameEventProposal():
    def __init__(self,game_event_proposal):
            # optional
            self.id:str = str(game_event_proposal.id) if getattr(game_event_proposal,"id") else None 
            self.accepted:bool = bool(game_event_proposal.accepted) if getattr(game_event_proposal,"accepted") else None 
            # repeated
            self.game_events:List = list()
            if getattr(game_event_proposal,"game_events"):
                game_events = game_event_proposal.game_events
                for game_event in game_events:
                    self.game_events.append(GameEvent(game_event))
        
class GameEvent():
    def __init__(self,game_event):
        #Oneof
        self.event = game_event.WhichOneof('event') 
        #optional
        self.id = game_event.id if getattr(game_event,"id") else None 
        self.type:enum = GameEventType(game_event.type) if getattr(game_event,"type") else None 
        self.created_timestamp = game_event.created_timestamp if getattr(game_event,"created_timestamp") else None 
        #repeated
        self.origin:List =list()
        if getattr(game_event,"origin") :
            origins = game_event.origin 
            for origin in origins:
                self.origin.append(str(origin))


class TeamInfo():
    def __init__(self,team):
        # Required
        self.name = str(team.name)
        self.score = int(team.score)
        self.red_cards = int(team.red_cards)
        self.yellow_cards = int(team.yellow_cards)
        self.timeouts = int(team.timeouts)
        self.timeout_time = int(team.timeout_time)
        self.goalkeeper = int(team.goalkeeper)
        
        ## Optional
        self.foul_counter = int(team.foul_counter) if getattr(team,"foul_counter") else None
        self.ball_placement_failures = int(team.ball_placement_failures) if getattr(team,"ball_placement_failures") else None
        self.can_place_ball = bool(team.can_place_ball) if getattr(team,"can_place_ball") else None
        self.max_allowed_bots = int(team.max_allowed_bots) if getattr(team,"max_allowed_bots") else None
        self.bot_substitution_intent = bool(team.bot_substitution_intent) if getattr(team,"bot_substitution_intent") else None
        self.ball_placement_failures_reached = bool(team.ball_placement_failures_reached) if getattr(team,"ball_placement_failures_reached") else None
        self.bot_substitution_allowed = bool(team.bot_substitution_allowed) if getattr(team,"bot_substitution_allowed") else None
        self.bot_substitutions_left = int(team.bot_substitutions_left) if getattr(team,"bot_substitutions_left") else None
        self.bot_substitution_time_left = int(team.bot_substitution_time_left) if getattr(team,"bot_substitution_time_left") else None
        
        ## repeated       

        self.yellow_card_times = list()
        if getattr(team,"yellow_card_times"):
            ycts = team.yellow_card_times
            for yct in ycts:
                self.yellow_card_times.append(int(yct))    
    
class RefereeMessage():
    def __init__(self,referee):
        self.packet_timestamp = int(referee.packet_timestamp)
        self.stage = Stage(referee.stage)
        self.command = Command(referee.command)
        self.command_cnt = int(referee.command_counter)
        self.command_ts = int(referee.command_timestamp)
        self.yellow = TeamInfo(referee.yellow)
        self.blue = TeamInfo(referee.blue)
        ## optional
        self.match_type = MatchType(referee.match_type) if getattr(referee,"match_type") else None        
        self.source_id = str(referee.source_identifier) if getattr(referee,"source_identifier") else None
        self.stage_time_left = int(referee.stage_time_left) if getattr(referee,"stage_time_left") else None
        self.designated_position = Point(referee.designated_position) if getattr(referee,"designated_position") else None
        self.blue_team_on_positive_half = bool(referee.blue_team_on_positive_half) if getattr(referee,"blue_team_on_positive_half") else None
        self.next_command = Command(referee.next_command) if getattr(referee,"next_command") else None
        self.current_action_time_remaining = int(referee.current_action_time_remaining) if getattr(referee,"current_action_time_remaining") else None
        self.status_message = str(referee.status_message) if getattr(referee,"status_message") else None
        
        ## repeated
        self.game_events = list()
        if getattr(referee,"game_events"):
            events = referee.game_events
            for num,event in enumerate(events):
                self.game_events.append(GameEvent(event))
            
        self.game_event_proposals = list()
        if getattr(referee,"game_event_proposals"):
           eps = referee.game_event_proposals  
           for ep in eps:
               self.game_event_proposals.append(GameEventProposal(ep))

        
        
       
if __name__ == "__main__":
    from TeamControl.Network.ssl_networking import GameControl
    
    gc_recv = GameControl()
    
    while True:
        ref_msg = gc_recv.listen()
        new_ref_msg = RefereeMessage(referee=ref_msg)
        print(ref_msg)

        print(f"{time.time()}\t{new_ref_msg.game_events[0].event}\t{(new_ref_msg.game_events[0].type)}\n")