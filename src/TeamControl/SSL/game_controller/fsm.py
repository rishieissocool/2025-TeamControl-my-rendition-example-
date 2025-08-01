from TeamControl.SSL.game_controller.Message import RefereeMessage,GameEvent
from TeamControl.SSL.game_controller.common import Command,Stage,GameEventType
from TeamControl.network.ssl_sockets import GameControl

from multiprocessing import Queue
from enum import Enum,auto

class PacketType(Enum):
    REMOVE_ROBOTS = auto()
    ADD_ROBOTS = auto()
    NEW_STATE = auto()
    SWITCH_TEAM = auto()
    BLF_LOCATION = auto()

class State(Enum) :
    PREPARE_FOR_GAME = auto()
    HALF_TIME = auto()
    TIMEOUT = auto()
    GAME_IS_RUNNING = auto()
    PENALTY_SHOOTOUT = auto()
    PREPARE_OUR_PENALTY = auto()
    PREPARE_THEIR_PENALTY = auto()
    PENALTY_SHOOTOUT_BREAK = auto()
    POST_GAME = auto()
    GAME_IS_HALTED = auto()
    GAME_IS_STOPPED = auto()
    PREPARE_KICKOFF = auto()
    FREE_KICK = auto()
    BALL_PLACEMENT = auto()
    
command_able_state = {State.GAME_IS_RUNNING,
                      State.PENALTY_SHOOTOUT_BREAK,
                      State.PENALTY_SHOOTOUT
                      }
    
class GCfsm ():
    def __init__(self,output_q:Queue,us_positive:bool=None,us_yellow:bool=None):
        self.output_q = output_q
        self.us_yellow = us_yellow
        self.us_positive = us_positive
        self.last_ref_msg = None
        # state, command, event, stage
        self.current_command = None
        self.current_event = None
        self.current_stage = None
        self.current_state = None
        # cards
        self.yellow_cards = 0
        self.yellow_card_active:int = 0
        self.red_cards = 0
        self.robots_away = 0

        # last known ball_left_field_location
        self.last_blf_location = None
        

    def update(self,new_ref_msg:RefereeMessage):
        # no previous packets
        if new_ref_msg.packet_timestamp < self.last_ref_msg.packet_timestamp:
            return 
        # otherwise :
        self.last_ref_msg = new_ref_msg
        self.check_color_side(new_ref_msg)
        self.check_cards(new_ref_msg)
        self.check_state(new_ref_msg)
        
    
            
    
    def check_cards(self,new_ref_msg:RefereeMessage):
        update_numbers = False
        if self.us_yellow is None or new_ref_msg.yellow is None or new_ref_msg.blue is None:
            return # no color identified = > do nothing
        
        yellow_cards = new_ref_msg.yellow.yellow_cards if self.us_yellow == True else new_ref_msg.blue.yellow_cards
        
        if self.yellow_cards != yellow_cards :  # number not equal
            print(f"yellow card number changed : {yellow_cards}")
            self.yellow_cards = yellow_cards
        
        yellow_card_active:int = len(new_ref_msg.yellow.yellow_card_times) if self.us_yellow==True else len(new_ref_msg.blue.yellow_card_times)

        if yellow_card_active != self.yellow_card_active:
            print(f"yellow card times changed : {yellow_card_active}")
            self.yellow_card_active = yellow_card_active
            update_numbers = True
        
        red_cards = new_ref_msg.yellow.red_cards if self.us_yellow == True else new_ref_msg.blue.red_cards
        if self.red_cards != red_cards : 
            print(f"red card number changed : {red_cards}")
            self.red_cards = red_cards
            update_numbers = True
        
        fouls = new_ref_msg.yellow.foul_counter if self.us_yellow == True else new_ref_msg.blue.foul_counter
        if self.fouls != fouls:
            print(f"Foul Counter has changed : {fouls}")
            self.fouls = fouls
            
        if update_numbers is True : 
            self.update_robot_numbers()
            
    def update_robot_numbers(self):
        robots_away = self.red_cards + self.yellow_card_active
        num =  robots_away - self.robots_away
        if num > 0:
            packet = (PacketType.REMOVE_ROBOTS,num)
        elif num < 0:
            packet = (PacketType.ADD_ROBOTS,abs(num))
        elif num == 0: 
            return
        self.robots_away = robots_away
        self.output_q.put(packet)
        
        
        
        
    def check_color_side(self,new_ref_msg:RefereeMessage):
        our_team_name :str = "TurtleRabbit"
        us_positive:bool = None
        us_yellow:bool = None
        
        if new_ref_msg.yellow.name == our_team_name:
            us_yellow = True
        elif new_ref_msg.blue.name == our_team_name:
            us_yellow = False
        
        # self.update_cards()
        
        if new_ref_msg.blue_team_on_positive_half is None:
            pass
        elif new_ref_msg.blue_team_on_positive_half is True:
            us_positive = False if  us_yellow == True else True
        elif new_ref_msg.blue_team_on_positive_half is False:
            us_positive = True if  us_yellow == True else False
        
        if self.us_yellow != us_yellow or self.us_positive != us_positive:
            packet = (PacketType.SWITCH_TEAM, {"YELLOW" : self.us_yellow,"POSITIVE": self.us_positive})
            self.output_q.put(packet)
            
        elif self.us_yellow is None:
            # warning log saying this is none
            # raise AttributeError ("US YELLOW = NONE -> need our TeamName")
            return
    
    
    def check_state(self,new_ref_msg:RefereeMessage):
        state_has_changed = False
        if new_ref_msg.command != self.current_command:
            state_has_changed = True
            self.current_command = new_ref_msg.command
            
        if new_ref_msg.stage != self.current_stage:
            state_has_changed = True
            self.current_stage = new_ref_msg.stage
        
       
        if state_has_changed is True:
            new_state = self.update_state()
            packet = (PacketType.NEW_STATE, new_state)
            self.output_q.put(packet)

    def check_game_events(self,new_ref_msg:RefereeMessage):
        game_events = new_ref_msg.game_events
        location = None
        if len(game_events) == 0:
            return
        
        for e in game_events:
            if e.type == GameEventType.BALL_LEFT_FIELD_TOUCH_LINE | GameEventType.BALL_LEFT_FIELD_GOAL_LINE:
                self.forward_ball_location(e.event_data)
                
    def forward_ball_location(self,event_data):
        location = event_data.location.vector
        if location is not None and self.last_blf_location != location:
                packet = (PacketType.BLF_LOCATION, location)
                self.output_q.put(packet)
                
    def update_state(self):
        stage_state = self._state_from_stage(self.current_stage)
        command_state = self._state_from_command(self.current_command)
        
        # if stage overrides everything
        if stage_state not in command_able_state:
            final_state = stage_state
        else:
            final_state = command_state or stage_state
        
        if final_state != self.current_state:
            # forward new state update
            packet = (PacketType.NEW_STATE, final_state)
            self.output_q.put(packet)
            # update new state in FSM 
            self.current_state = final_state
    
    def _state_from_stage(self):
        match self.current_stage:
            case Stage.NORMAL_FIRST_HALF_PRE  | Stage.NORMAL_SECOND_HALF_PRE | Stage.EXTRA_FIRST_HALF_PRE | Stage.EXTRA_SECOND_HALF_PRE:
                state = State.PREPARE_FOR_GAME
                
            case Stage.NORMAL_FIRST_HALF | Stage.NORMAL_SECOND_HALF | Stage.EXTRA_FIRST_HALF | Stage.EXTRA_HALF_TIME:
                state = State.GAME_IS_RUNNING
                
            case Stage.EXTRA_HALF_TIME | Stage.NORMAL_HALF_TIME:
                state = State.HALF_TIME
        
            case Stage.PENALTY_SHOOTOUT : 
                state = State.PENALTY_SHOOTOUT
                
            case Stage.PENALTY_SHOOTOUT_BREAK : 
                state = State.PENALTY_SHOOTOUT_BREAK
            
            case Stage.POST_GAME:
                state = State.POST_GAME
    
        return state
    
    def _state_from_command(self):
        ### COMMAND ###
        match self.current_command: 
            case Command.HALT:
                state = State.GAME_IS_HALTED 
            case Command.STOP:
                state = State.GAME_IS_STOPPED
            case Command.NORMAL_START | Command.FORCE_START:
                state = State.GAME_IS_RUNNING
            
            ## YELLOW ##
            case Command.DIRECT_FREE_YELLOW | Command.INDIRECT_FREE_YELLOW:
                if self.us_yellow == True:
                    state = State.FREE_KICK
                else:
                    state = State.GAME_IS_HALTED
            case Command.PREPARE_KICKOFF_YELLOW:
                if self.us_yellow == True:
                    state = State.PREPARE_KICKOFF
                else:
                    state = State.GAME_IS_HALTED
            case Command.BALL_PLACEMENT_YELLOW:
                if self.us_yellow == True:
                    state = State.BALL_PLACEMENT
                else:
                    state = State.GAME_IS_HALTED
                    
            case Command.PREPARE_PENALTY_YELLOW: 
                if self.us_yellow == True:
                    state = State.PREPARE_OUR_PENALTY
                else:
                    state = State.PREPARE_THEIR_PENALTY
            case Command.TIMEOUT_YELLOW:
                if self.us_yellow == True:
                    state = State.TIMEOUT
                else: 
                    state = State.PREPARE_FOR_GAME
            
            ## BLUE ## 
            case Command.DIRECT_FREE_BLUE | Command.INDIRECT_FREE_BLUE:
                if self.us_yellow == False:
                    state = State.FREE_KICK
                else:
                    state = State.GAME_IS_HALTED
            case Command.PREPARE_KICKOFF_BLUE:
                if self.us_yellow == False:
                    state = State.PREPARE_KICKOFF
                else:
                    state = State.GAME_IS_HALTED
            case Command.BALL_PLACEMENT_BLUE:
                if self.us_yellow == False:
                    state = State.BALL_PLACEMENT
                else:
                    state = State.GAME_IS_HALTED
                    
            case Command.PREPARE_PENALTY_BLUE: 
                if self.us_yellow == False:
                    state = State.PREPARE_OUR_PENALTY
                else:
                    state = State.PREPARE_THEIR_PENALTY
                    
            case Command.TIMEOUT_BLUE:
                if self.us_yellow == False:
                    state = State.TIMEOUT
                else: 
                    state = State.PREPARE_FOR_GAME
            
        return state



def run_gcfsm(output_q,us_yellow=None,us_positive=None): #Process for multiprocess
    fsm = GCfsm(output_q=output_q,us_yellow=us_yellow,us_positive=us_positive)
    gcl = GameControl()
    while True: 
        raw_ref_msg = gcl.listen() # listens overnetwork
        new_ref_msg = RefereeMessage(raw_ref_msg) # format into class
        fsm.update(new_ref_msg) # updates state machine
    
    