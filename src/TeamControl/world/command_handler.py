from TeamControl.SSL.game_controller.common import *
import enum 
class STATE(Enum):
    RUNNING = 0
    HALTED = 1
    STOPPED = 2
    TIMEOUT = 3

    def update_stage(self,stage):
        print(stage)
        match stage:
            case Stage.NORMAL_FIRST_HALF_PRE :
                return prepare_for_game
            case Stage.NORMAL_SECOND_HALF_PRE :
                return prepare_for_game
            case Stage.NORMAL_FIRST_HALF :
                return run
            case Stage.NORMAL_HALF_TIME :
                return timeout
            case Stage.NORMAL_SECOND_HALF :
                return 
            case Stage.EXTRA_TIME_BREAK :
                return 
            case Stage.EXTRA_FIRST_HALF_PRE :
                return 
            case Stage.EXTRA_FIRST_HALF :
                return 
            case Stage.EXTRA_HALF_TIME :
                return 
            case Stage.EXTRA_SECOND_HALF_PRE :
                return 
            case Stage.EXTRA_SECOND_HALF :
                return 
            case  Stage.PENALTY_SHOOTOUT_BREAK :
                return timeout
            case  Stage.PENALTY_SHOOTOUT :
                return penalty_shoot
            case Stage.POST_GAME :
                return post_game

    
    def update_state(self,command):
        print(command) 
        match command:
            case Command.HALT:
                return STATE.HALTED
            case Command.STOP:
                return STATE.STOPPED
            case Command.NORMAL_START | Command.FORCE_START:
                return STATE.RUNNING
            
            case Command.TIMEOUT_BLUE:
                return 
            case Command.TIMEOUT_YELLOW:
                return 
            case Command.BALL_PLACEMENT_BLUE:
                return
            case Command.PREPARE_KICKOFF_BLUE:
                return
            case Command.PREPARE_PENALTY_BLUE:
                return
            
            case Command.DIRECT_FREE_BLUE:
                return
            case Command.INDIRECT_FREE_BLUE:
                return
            
            case Command.BALL_PLACEMENT_YELLOW:
                return
            case Command.PREPARE_KICKOFF_YELLOW:
                return
            case Command.PREPARE_PENALTY_YELLOW:
                return
            
            case Command.DIRECT_FREE_YELLOW:
                return
            case Command.INDIRECT_FREE_YELLOW:
                return