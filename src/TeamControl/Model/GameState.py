import logging
import enum
from enum import auto, unique
from typing import Optional, Union, List
from dataclasses import dataclass, field

log = logging.getLogger()
log.setLevel(logging.NOTSET)



class GameControllerCommand(enum.Enum):
    HALT = auto()
    STOP = auto()
    NORMAL_START = auto()
    FORCE_START = auto()
    PREPARE_KICKOFF_YELLOW = auto()
    PREPARE_KICKOFF_BLUE = auto()
    PREPARE_PENALTY_YELLOW = auto()
    PREPARE_PENALTY_BLUE = auto()
    DIRECT_FREE_YELLOW = auto() 
    DIRECT_FREE_BLUE = auto()
    INDIRECT_FREE_YELLOW = auto() #depeciated
    INDIRECT_FREE_BLUE = auto() #depeciated
    TIMEOUT_YELLOW = auto()
    TIMEOUT_BLUE = auto()
    GOAL_YELLOW = auto() #depeciated
    GOAL_BLUE = auto() #depeciated
    BALL_PLACEMENT_YELLOW = auto()
    BALL_PLACEMENT_BLUE = auto()
    UNKNOWN_COMMAND = auto()

class GameEventType(enum.Enum):
    UNKNOWN_GAME_EVENT = auto()

    BALL_LEFT_FIELD_TOUCH_LINE = auto()
    BALL_LEFT_FIELD_GOAL_LINE = auto()

    AIMLESS_KICK = auto()

    ATTACKER_TOO_CLOSE_TO_DEFENSE_AREA = auto()
    DEFENDER_IN_DEFENSE_AREA = auto()
    BOUNDARY_CROSSING = auto()
    KEEPER_HELD_BALL = auto()
    BOT_DRIBBLED_BALL_TOO_FAR = auto()

    BOT_PUSHED_BOT = auto()
    BOT_HELD_BALL_DELIBERATELY = auto()
    BOT_TRIPPED_OVER = auto()
    BOT_DROPPED_PARTS = auto()

    ATTACKER_TOUCHED_BALL_IN_DEFENSE_AREA = auto()
    BOT_KICKED_BALL_TOO_FAST = auto()
    BOT_CRASH_UNIQUE = auto()
    BOT_CRASH_DRAWN = auto()

    DEFENDER_TOO_CLOSE_TO_KICK_POINT = auto()
    BOT_TOO_FAST_IN_STOP = auto()
    BOT_INTERFERED_PLACEMENT = auto()
    EXCESSIVE_BOT_SUBSTITUTION = auto()
    
    POSSIBLE_GOAL = auto()
    GOAL = auto()
    INVALID_GOAL = auto()

    ATTACKER_DOUBLE_TOUCHED_BALL = auto()
    PLACEMENT_SUCCEEDED = auto()
    PENALTY_KICK_FAILED = auto()
    
    NO_PROGRESS_IN_GAME = auto()
    PLACEMENT_FAILED = auto()
    MULTIPLE_CARDS = auto()
    MULTIPLE_FOULS = auto()
    BOT_SUBSTITUTION = auto()
    TOO_MANY_ROBOTS = auto()
    CHALLENGE_FLAG = auto()
    CHALLENGE_FLAG_HANDLED = auto()
    EMERGENCY_STOP = auto()

    UNSPORTING_BEHAVIOR_MINOR = auto()
    UNSPORTING_BEHAVIOR_MAJOR = auto()

    PREPARED = auto()
    INDIRECT_GOAL = auto()
    CHIPPED_GOAL = auto()
    KICK_TIMEOUT = auto()
    ATTACKER_TOUCHED_OPPONENT_IN_DEFENSE_AREA = auto()
    ATTACKER_TOUCHED_OPPONENT_IN_DEFENSE_AREA_SKIPPED = auto()
    BOT_CRASH_UNIQUE_SKIPPED = auto()
    BOT_PUSHED_BOT_SKIPPED = auto()
    DEFENDER_IN_DEFENSE_AREA_PARTIALLY = auto()
    MULTIPLE_PLACEMENT_FAILURE = auto()

    __deprecated__ = [
        'PREPARED',
        'INDIRECT_GOAL',
        'CHIPPED_GOAL',
        'KICK_TIMEOUT', 
        'ATTACKER_TOUCHED_OPPONENT_IN_DEFENSE_AREA',
        'ATTACKER_TOUCHED_OPPONENT_IN_DEFENSE_AREA_SKIPPED',
        'BOT_CRASH_UNIQUE_SKIPPED',
        'BOT_PUSHED_BOT_SKIPPED',
        'DEFENDER_IN_DEFENSE_AREA_PARTIALLY',
        'MULTIPLE_PLACEMENT_FAILURE',
    ]

class Stage(enum.IntEnum):
    NORMAL_FIRST_HALF_PRE = auto()
    NORMAL_FIRST_HALF = auto()
    NORMAL_HALF_TIME = auto()
    NORMAL_SECOND_HALF_PRE = auto()
    NORMAL_SECOND_HALF = auto()
    EXTRA_TIME_BREAK = auto()
    EXTRA_FIRST_HALF_PRE = auto()
    EXTRA_FIRST_HALF = auto()
    EXTRA_HALF_TIME = auto()
    EXTRA_SECOND_HALF_PRE = auto()
    EXTRA_SECOND_HALF = auto()
    PENALTY_SHOOTOUT_BREAK = auto()
    PENALTY_SHOOTOUT = auto()
    POST_GAME = auto()

class Match(enum.Enum):
    UNKNOWN_MATCH = auto()
    GROUP_PHASE = auto()
    ELIMINATION_PHASE = auto()
    FRIENDLY = auto()

# do not use frozen=True if you see = None or = field(default_factory) or = field(default)


@dataclass(frozen=True)
class Point:
    x: float
    y: float

@dataclass #(frozen=True)
class GameEventProposalGroup :
    id: str
    gameEvents:List[GameEventType] = field(default_factory=list)
    accepted: bool = None


@dataclass (order=True) #(frozen=True)
class TeamInfo:
    name: str 
    score: int = None
    redCards: int = None
    yellowCards: int = None
    yellowCardTimes:list[int] = field(default_factory=list)
    timeouts: int = None
    timeoutTime: int = None
    goalkeeper: int = None
    foulCounter: Optional[int] = None
    ballPlacementFailures: Optional[int] = None
    canPlaceBall: Optional[bool] = None
    maxAllowedBots: Optional[int] = None
    botSubstitutionIntent: Optional[bool] = None
    ballPlacementFailuresReached: Optional[bool] = None
    botSubstitutionAllowed: Optional[bool] = None
    botSubstitutionsLeft: Optional[int] = None
    botSubstitutionTimeLeft: Optional[int] = None
    
@dataclass (order=True) #(frozen=True)
class State:
    packetTimestamp: int = None
    stage: Stage = None
    stageTimeLeft: Optional[int] = None
    command: GameControllerCommand = None
    commandCounter: int = None
    commandTimestamp: int = None
    yellow: TeamInfo = None
    blue: TeamInfo = None
    designatedPosition: Optional[Point] = None
    blueTeamOnPositiveHalf: Optional[bool] = None
    # game_event: GameEventType # Depeciated and reserved
    nextCommand: Optional[GameControllerCommand] = None
    gameEvents: List[GameEventType] = field(default_factory=list)
    gameEventProposals: List[GameEventProposalGroup] = field(default_factory=list)
    currentActionTimeRemaining: Optional[int] = None
    status_message: Optional[str] = None
    sourceIdentifier: Optional[str] = None
    matchType: Optional[Match] = None

    def __post_init__(self):
        y = self.yellow
        self.yellow = TeamInfo(**y)
        b = self.blue
        self.blue = TeamInfo(**b)
        print (type(self.yellow), self.yellow)

if __name__ == "__main__":
    from TeamControl.Network.ssl_networking import GameControl
    
    referee_l = GameControl()
    
    state = referee_l.listen()
