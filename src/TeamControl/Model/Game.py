""" Game.py 
Stores only the field of ref message we need
"""
from TeamControl.Model.GameState import *
import enum
import typing
from typing import Optional, List, Union
import time


class GameEventProposal():
    def __init__(self,game_event_proposal):
            # optional
            self.id:str = str(game_event_proposal.id) if getattr(game_event_proposal,"id") else None 
            self.accepted:bool = bool(game_event_proposal.accepted) if getattr(game_event_proposal,"accepted") else None 
            # repeated
            self.game_events = [GameEvent(game_event) for game_event in getattr(game_event_proposal, "game_events", [])]
 
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
        self.yellow_card_times = [int(yellow_card_time) for yellow_card_time in getattr(team, "yellow_card_times", [])]

    
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
        self.game_events = [GameEvent(game_event) for game_event in getattr(referee, "game_events", [])]
        self.game_event_proposals = [GameEventProposal(game_event_proposal) for game_event_proposal in getattr(referee, "game_event_proposal", [])]

        
        
       
if __name__ == "__main__":
    from TeamControl.Network.ssl_networking import GameControl
    
    gc_recv = GameControl()
    
    while True:
        ref_msg = gc_recv.listen()
        start_time = time.time()
        new_ref_msg = RefereeMessage(referee=ref_msg)
        print(ref_msg)
        print(f"internal process time :{time.time()-start_time}\t\n"+
              f"recv + process time :{time.time()-new_ref_msg.packet_timestamp/1000000}\t\n"+
              f"{(new_ref_msg.game_events[0].by_team)}\t  {type(new_ref_msg.game_events[0].type)}\n"
              )