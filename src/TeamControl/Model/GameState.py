import logging
import enum
from enum import auto, unique
from typing import Optional, Union, List


class Command(enum.Enum):
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

class Team(enum.Enum):
    BLUE = auto()
    YELLOW = auto()
    
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

class MatchType(enum.Enum):
    UNKNOWN_MATCH = auto()
    GROUP_PHASE = auto()
    ELIMINATION_PHASE = auto()
    FRIENDLY = auto()