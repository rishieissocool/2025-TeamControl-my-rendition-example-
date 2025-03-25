""" Game.py 
Stores only the field of ref message we need
"""
from TeamControl.Model.GameState import *
import enum
import typing
from typing import Optional, List, Union

    
class GameEventProposal():
    def __init__(self, id:str=None, game_events=None, accepted:bool=None):
        if game_events is not None:
            self.id = id
            self.game_events = GameEvent(game_events)
            self.accepted:bool = accepted
        

class GameEvent():
    def __init__(self,game_event):
        # self.event = 
        self.id = game_event.id
        self.type:enum = GameEventType(game_event.type)
        self.origin = game_event.origin
        self.created_timestamp = game_event.created_timestamp

class YellowCard():
    def __init__(self,YellowCard):
        self.id = int(YellowCard.id) if getattr(YellowCard,"id") else None 
        self.caused_by_game_event = GameEvent(YellowCard.caused_by_game_event) if getattr(YellowCard,"caused_by_game_event") else None
        self.time_remaining = float(YellowCard.time_remaining) if getattr(YellowCard,"time_remaining") else None

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
        self.bot_substitution_left = int(team.bot_substitution_left) if getattr(team,"bot_substitution_left") else None
        self.bot_substitution_time_left = int(team.bot_substitution_time_left) if getattr(team,"bot_substitution_time_left") else None
        
        ## repeated       
        self.yellow_card_times = int(team.yellow_card_times) if getattr(team,"yellow_card_times") else None
    
    
class RefereeMessage():
    def __init__(self, packet_timestamp:int,stage:enum,cmd:Command,cmd_counter:int,
                 cmd_timestamp:int,yellow:TeamInfo, blue:TeamInfo, 
                 source_id=None,match_type:enum=None,stage_time_left:int=None,
                 designated_pos=None,blue_on_positive_half:bool=None,next_cmd=None, 
                 game_events=list(), game_events_proposal: List[GameEvent]=list(), 
                 current_action_time_remaining:int=None, status_message=""):
        
        self.packet_timestamp:int = packet_timestamp
        self.match_type = match_type
        self.source_id = source_id
        self.stage:enum = stage.name
        self.stage_time_left=stage_time_left
        self.cmd = cmd
        self.cmd_counter = cmd_counter
        self.cmd_timestamp = cmd_timestamp
        self.yellow = yellow
        self.blue = blue
        self.designated_pos = designated_pos
        self.blue_on_positive_half = blue_on_positive_half
        self.next_cmd = next_cmd
        self.game_events = GameEvent(game_events)
        self.game_events_proposal = GameEventProposal(game_events_proposal)
        self.current_action_time_remaining:int = current_action_time_remaining
        self.status_message = status_message
    
    @staticmethod
    def set(referee): 
        packet_timestamp = int(referee.packet_timestamp)
        stage = Stage(referee.stage)
        command = Command(referee.command)
        command_cnt = referee.command_counter
        command_ts = referee.command_timestamp
        yellow = TeamInfo(referee.yellow)
        blue = TeamInfo(referee.blue)
        print(yellow.name)
        ## optional
        match_type = MatchType(referee.match_type) if getattr(referee,"match_type") else None        
        source_id = referee.source_identifier if getattr(referee,"source_identifier") else None
        stage_time_left = referee.stage_time_left if getattr(referee,"stage_time_left") else None
        designated_position = referee.designated_position if getattr(referee,"designated_position") else None
        blue_team_on_positive_half = referee.blue_team_on_positive_half if getattr(referee,"blue_team_on_positive_half") else None
        next_command = Command(referee.next_command) if getattr(referee,"next_command") else None
        current_action_time_remaining = referee.current_action_time_remaining if getattr(referee,"current_action_time_remaining") else None
        status_message = referee.status_message if getattr(referee,"status_message") else None
        
        ## repeated
        game_events = list()
        if getattr(referee,"game_events"):
            events = referee.game_events  
            for num,event in enumerate(events):
                game_events.append(GameEvent(event))
                
            
        game_event_proposals = referee.game_event_proposals if getattr(referee,"game_event_proposals") else list()
        
        
        RefereeMessage(packet_timestamp=packet_timestamp,stage=stage,
                    cmd=command, cmd_counter=command_cnt,cmd_timestamp=command_ts,
                    yellow=yellow, blue=blue, 
                    source_id=source_id,match_type=match_type,stage_time_left=stage_time_left,
                    designated_pos=designated_position,blue_on_positive_half=blue_team_on_positive_half,
                    next_cmd=next_command,game_events=game_events, game_events_proposal=game_event_proposals, 
                    current_action_time_remaining=current_action_time_remaining, status_message=status_message)

if __name__ == "__main__":
    from TeamControl.Network.ssl_networking import GameControl
    
    gc_recv = GameControl()
    
    while True:
        ref_msg = gc_recv.listen()
        new_ref_msg = RefereeMessage.set(ref_msg)