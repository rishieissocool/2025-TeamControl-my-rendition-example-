import logging
import enum
from enum import auto, unique
from typing import Union

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
    INDIRECT_FREE_YELLOW = auto()
    INDIRECT_FREE_BLUE = auto()
    TIMEOUT_YELLOW = auto()
    TIMEOUT_BLUE = auto()
    GOAL_YELLOW = auto()
    GOAL_BLUE = auto()
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

class Match(enum.Enum):
    UNKNOWN_MATCH = auto()
    GROUP_PHASE = auto()
    ELIMINATION_PHASE = auto()
    FRIENDLY = auto()

class Point:
    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int) -> None:
        if not isinstance(x, int):
            log.error("attribute `Point.x` is not an object of type `int`")
        self._x = x
    
    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        if not isinstance(y, int):
            log.error("attribute `Point.y` is not an object of type `int`")
        self._y = y

    def __repr__(self):
        return f"Point\n\t\t x={self.x}\n\t\t y={self.y}"

class Event:
    def __init__(self, id: str, type: int, origin: str, created_timestamp: int) -> None:
        self.id = id
        self.type = type
        self.origin = origin
        self.created_timestamp = created_timestamp

    def ball_left_field(self, by_team: Team, by_bot: int, location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location

    def aimless_kick(self, by_team: Team, by_bot: int, location: Point, kick_location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.kick_location = kick_location

    def goal(self, by_team: Team, kicking_team: Team = None, location: Point = None, 
             kick_location: Point = None, max_ball_height: float = None, num_robots_by_team: Team = None, 
             last_touch_by_team: Team = None, message: str = None) -> None:
        self.by_team = by_team
        self.kicking_team = kicking_team
        self.location = location 
        self.kick_location = kick_location
        self.max_ball_height = max_ball_height
        self.num_robots_by_team = num_robots_by_team
        self.last_touch_by_team = last_touch_by_team
        self.message = message

    def indirect_goal(self, by_team: Team, by_bot: int, location: Point, kick_location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location 
        self.kick_location = kick_location

    def chipped_goal(self, by_team: Team, by_bot: int, location: Point, kick_location: Point, max_ball_height: float) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.kick_location = kick_location
        self.max_ball_height = max_ball_height

    def bot_too_fast_in_stop(self, by_team: Team, by_bot: int, location: Point, speed: float) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.speed = speed

    def defender_too_close_to_kick_point(self, by_team: Team, by_bot: int, location: Point, distance: float) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.distance = distance

    def bot_crash_drawn(self, bot_yellow: int, bot_blue: int, location: Point,
                        crash_speed: float, speed_diff: float, crash_angle: float) -> None:
        self.bot_yellow = bot_yellow
        self.bot_blue = bot_blue
        self.location = location
        self.crash_speed = crash_speed
        self.speed_diff = speed_diff
        self.crash_angle = crash_angle

    def bot_crash_unique(self, by_team: Team, violator: int, victim: int, location: Point,
                         crash_speed: float, speed_diff: float, crash_angle: float) -> None:
        self.by_team = by_team
        self.violator = violator
        self.victim = victim
        self.location = location
        self.crash_speed = crash_speed
        self.speed_diff = speed_diff
        self.crash_angle = crash_angle

    def bot_push_bot(self, by_team: Team, violator: int, victim: int, location: Point, 
                     distance: float) -> None:
        self.by_team = by_team
        self.violator = violator
        self.victim = victim
        self.location = location
        self.distance = distance

    def bot_tripped_over(self, by_team: Team, by_bot: int, location: Point, ball_location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.ball_location = ball_location

    def bot_dropped_parts(self, by_team: Team, by_bot: int, location: Point, ball_location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.ball_location = ball_location

    def defender_in_defense_area_partially(self, by_team: Team, by_bot: int, location: Point, ball_location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.ball_location = ball_location

    def attacker_touched_ball_in_defense_area(self, by_team: Team, by_bot: int, location: Point, distance: float) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.distance = distance

    def bot_kicked_ball_too_fast(self, by_team: Team, by_bot: int, location: Point, initial_ball_speed: float, chipped: bool) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location
        self.initial_ball_speed = initial_ball_speed
        self.chipped = chipped

    def bot_dribbled_ball_too_far(self, by_team: Team, by_bot: int, start: Point, end: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.start = start
        self.end = end

    def attacker_touched_opponent_in_defense_area(self, by_team: Team, by_bot: int, victim: int, location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.victim = victim
        self.location = location

    def attacker_double_touched_ball(self, by_team: Team, by_bot: int, location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location

    def attacker_too_close_to_defense_area(self, by_team: Team, by_bot: int, distance: float, ball_location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.distance = distance
        self.ball_location = ball_location

    def bot_held_ball_deliberately(self, by_team: Team, by_bot: int, distance: float, duration: float) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.distance = distance
        self.duration = duration

    def bot_interfered_placement(self, by_team: Team, by_bot: int, location: Point) -> None:
        self.by_team = by_team
        self.by_bot = by_bot
        self.location = location

    def multiple_cards(self, by_team: Team) -> None:
        self.by_team = by_team

    def multiple_fouls(self, by_team: Team, caused_game_events: list) -> None:
        self.by_team = by_team
        self.caused_game_events = caused_game_events

    def multiple_placement_failure(self, by_team: Team) -> None:
        self.by_team = by_team

    def multiple_placement_failure(self, by_team: Team, location: Point, time: float) -> None:
        self.by_team = by_team
        self.location = location
        self.time = time

    def no_progress_in_game(self, location: Point, time: float) -> None:
        self.location = location
        self.time = time

    def placement_failure(self, by_team: Team, remaining_distance: float, nearest_own_bot_distance: float) -> None:
        self.by_team = by_team
        self.remaining_distance = remaining_distance
        self.nearest_own_bot_distance = nearest_own_bot_distance

    def unsporting_behavior_minor(self, by_team: Team, reason: str) -> None:
        self.by_team = by_team
        self.reason = reason

    def unsporting_behavior_major(self, by_team: Team, reason: str) -> None:
        self.by_team = by_team
        self.reason = reason

    def keeper_held_ball(self, by_team: Team, location: Point, duration: float) -> None:
        self.by_team = by_team
        self.location = location
        self.duration = duration

    def placement_succeeded(self, by_team: Team, time_taken: float, precision: float, distance: float) -> None:
        self.by_team = by_team
        self.time_taken = time_taken
        self.precision = precision
        self.distance = distance

    def prepared(self, time_taken: float) -> None:
        self.time_taken = time_taken

    def bot_substitution(self, by_team: Team) -> None:
        self.by_team = by_team

    def excessive_bot_substitution(self, by_team: Team) -> None:
        self.by_team = by_team

    def challenge_flag(self, by_team: Team):
        self.by_team = by_team

    def challenge_flag_handled(self, by_team: Team, accepted: bool) -> None:
        self.by_team = by_team
        self.accepted = accepted

    def emergency_stop(self, by_team: Team) -> None:
        self.by_team = by_team

    def too_many_robots(self, by_team: Team, num_robots_allowed: int, num_robots_on_field: int, ball_location: Point) -> None:
        self.by_team = by_team
        self.num_robots_allowed = num_robots_allowed
        self.num_robots_on_field = num_robots_on_field
        self.ball_location = ball_location

    def boundary_crossing(self, by_team: Team, location: Point) -> None:
        self.by_team = by_team
        self.location = location

    def penalty_kick_failed(self, by_team: Team, location: Point, reason: str) -> None:
        self.by_team = by_team
        self.location = location
        self.reason = reason 
    
    @property
    def game_event_type(self) -> GameEventType:
        return self._game_event_type

    @game_event_type.setter
    def type(self, game_event_type: GameEventType) -> None:
        if not isinstance(game_event_type, GameEventType):
            log.error("attribute `Event.game_event_type` is not an object of type `GameEventType`")
        self._game_event_type = game_event_type
    
    def __repr__(self) -> str:
        string = "\n"
        for k in self.__dict__.keys():
            string += f"\t\t\033[0;33m{k}\033[0m: {repr(self.__dict__[k])}\n"
        return string
    
    def __setattr__(self, name, value) -> None:
        match name:
            case 'by_team' | 'kicking_team':
                value = Team[value]
            case 'location' | 'kick_location' | 'ball_location' | 'start' | 'end':
                if not value is None:
                    x = value['x']
                    y = value['y']

                    value = Point()
                    value.x = x
                    value.y = y
                else:
                    log.warning(f'class Event.{name} defaulted to None')
            
        object.__setattr__(self, name, value)

class EventFactory:
    @staticmethod
    def get_event_factory_function(event: Event) -> callable:              
            match event.game_event_type:
                case GameEventType.BALL_LEFT_FIELD_TOUCH_LINE:
                    return event.ball_left_field
                case GameEventType.BALL_LEFT_FIELD_GOAL_LINE:
                    return event.ball_left_field
                case GameEventType.AIMLESS_KICK:
                    return event.aimless_kick
                case GameEventType.ATTACKER_TOO_CLOSE_TO_DEFENSE_AREA:
                    return event.attacker_touched_ball_in_defense_area
                case GameEventType.DEFENDER_IN_DEFENSE_AREA:
                    return event.defender_in_defense_area_partially
                case GameEventType.BOUNDARY_CROSSING:
                    return event.boundary_crossing
                case GameEventType.KEEPER_HELD_BALL:
                    return event.keeper_held_ball
                case GameEventType.BOT_DRIBBLED_BALL_TOO_FAR:
                    return event.bot_dribbled_ball_too_far
                case GameEventType.BOT_PUSHED_BOT:
                    return event.bot_push_bot
                case GameEventType.BOT_HELD_BALL_DELIBERATELY:
                    return event.bot_held_ball_deliberately
                case GameEventType.BOT_TRIPPED_OVER:
                    return event.bot_tripped_over
                case GameEventType.BOT_DROPPED_PARTS:
                    return event.bot_dropped_parts
                case GameEventType.ATTACKER_TOUCHED_BALL_IN_DEFENSE_AREA:
                    return event.attacker_too_close_to_defense_area
                case GameEventType.BOT_KICKED_BALL_TOO_FAST:
                    return event.bot_kicked_ball_too_fast
                case GameEventType.BOT_CRASH_UNIQUE:
                    return event.bot_crash_unique
                case GameEventType.BOT_CRASH_DRAWN:
                    return event.bot_crash_drawn
                case GameEventType.DEFENDER_TOO_CLOSE_TO_KICK_POINT:
                    return event.defender_too_close_to_kick_point
                case GameEventType.BOT_TOO_FAST_IN_STOP:
                    return event.bot_too_fast_in_stop
                case GameEventType.BOT_INTERFERED_PLACEMENT:
                    return event.bot_interfered_placement
                case GameEventType.EXCESSIVE_BOT_SUBSTITUTION:
                    return event.excessive_bot_substitution
                case GameEventType.POSSIBLE_GOAL:
                    return event.goal
                case GameEventType.GOAL:
                    return event.goal
                case GameEventType.INVALID_GOAL:
                    return event.goal
                case GameEventType.ATTACKER_DOUBLE_TOUCHED_BALL:
                    return event.attacker_double_touched_ball
                case GameEventType.PLACEMENT_SUCCEEDED:
                    return event.placement_succeeded
                case GameEventType.PENALTY_KICK_FAILED:
                    return event.penalty_kick_failed
                case GameEventType.NO_PROGRESS_IN_GAME:
                    return event.no_progress_in_game
                case GameEventType.PLACEMENT_FAILED:
                    return event.placement_failure
                case GameEventType.MULTIPLE_CARDS:
                    return event.multiple_cards
                case GameEventType.MULTIPLE_FOULS:
                    return event.multiple_fouls
                case GameEventType.BOT_SUBSTITUTION:
                    return event.bot_substitution
                case GameEventType.TOO_MANY_ROBOTS:
                    return event.too_many_robots
                case GameEventType.CHALLENGE_FLAG:
                    return event.challenge_flag
                case GameEventType.CHALLENGE_FLAG_HANDLED:
                    return event.challenge_flag_handled
                case GameEventType.EMERGENCY_STOP:
                    return event.emergency_stop
                case GameEventType.UNSPORTING_BEHAVIOR_MINOR:
                    return event.unsporting_behavior_minor
                case GameEventType.UNSPORTING_BEHAVIOR_MAJOR:
                    return event.unsporting_behavior_major
    
    @staticmethod
    def __call__(json) -> Event:
        id = json['id']
        game_event_type = GameEventType[json['type']]
        if game_event_type in GameEventType.__deprecated__:
            log.warning(f'{game_event_type} Event is deprecated')
        origin = json['origin']
        created_timestamp = json['created_timestamp']
        event = Event(id, game_event_type, origin, created_timestamp)
        generator = EventFactory.get_event_factory_function(event)
        kwargs = json[json['type'].lower()]
        generator(**kwargs)
        return event

class TeamInformation:
    @property
    def name(self) -> str:
        return self._name
    
    @property       
    def score(self) -> int:
        return self._score
    
    @property
    def red_cards(self) -> int:
        return self._red_cards
    
    @property
    def yellow_cards(self) -> int:
        return self._yellow_cards
    
    @property
    def timeouts(self) -> int:
        return self._timeouts
    
    @property
    def timeout_time(self) -> int:
        return self._timeout_time
    
    @property
    def goalkeeper(self) -> int:
        return self._goalkeeper 
    
    @property
    def foul_counter(self) -> int:
        return self._foul_counter 
    
    @property
    def ball_placement_failures(self) -> int:
        return self._ball_placement_failures
    
    @property
    def can_place_ball(self) -> bool:
        return self._can_place_ball 
    
    @property
    def max_allowed_bots(self) -> int:
        return self._max_allowed_bots 
    
    @property
    def bot_substitution_intent(self) -> bool:
        return self._bot_substitution_intent 
    
    @property
    def ball_placement_failures_reached(self) -> bool:
        return self._ball_placement_failures_reached 
    
    @property
    def bot_substitution_allowed(self) -> bool:
        return self._bot_substitution_allowed 
    
    @property
    def bot_substitutions_left(self) -> int:
        return self._bot_substitutions_left 
    
    @property
    def bot_substitution_time_left(self) -> int:
        return self._bot_substitution_time_left
    
    @name.setter
    def name(self, name):    
        if not isinstance(name, str):
           log.error('attribute `name` is not an object of type `str`')
        self._name = name
    
    @score.setter      
    def score(self, score: int) -> None:
        if not isinstance(score, int):
           log.error('attribute `score` is not an object of type `int`')
        self._score = score
    
    @red_cards.setter
    def red_cards(self, red_cards: int) -> None:
        if not isinstance(red_cards, int):
           log.error('attribute `red_cards` is not an object of type `int`')
        self._red_cards = red_cards
    
    @yellow_cards.setter
    def yellow_cards(self, yellow_cards: int) -> None:
        if not isinstance(yellow_cards, int):
           log.error('attribute `yellow_cards` is not an object of type `int`')
        self._yellow_cards = yellow_cards
    
    @timeouts.setter
    def timeouts(self, timeouts: int) -> None:
        if not isinstance(timeouts, int):
           log.error('attribute `timeouts` is not an object of type `int`')
        self._timeouts = timeouts
    
    @timeout_time.setter
    def timeout_time(self, timeout_time: int) -> None:
        if not isinstance(timeout_time, int):
           log.error('attribute `timeout_time` is not an object of type `int`')
        self._timeout_time = timeout_time
    
    @goalkeeper.setter
    def goalkeeper(self, goalkeeper: int) -> None:
        if not isinstance(goalkeeper, int):
           log.error('attribute `goalkeeper` is not an object of type `int`')
        self._goalkeeper = goalkeeper 
    
    @foul_counter.setter
    def foul_counter(self, foul_counter: int) -> None:
        if not isinstance(foul_counter, int):
           log.error('attribute `foul_counter` is not an object of type `int`')
        self._foul_counter = foul_counter 
    
    @ball_placement_failures.setter
    def ball_placement_failures(self, ball_placement_failures: int) -> None:
        if not isinstance(ball_placement_failures, int):
           log.error('attribute `ball_placement_failures` is not an object of type `int`')
        self._ball_placement_failures = ball_placement_failures 
    
    @can_place_ball.setter
    def can_place_ball(self, can_place_ball: int) -> None:
        if not isinstance(can_place_ball, int):
           log.error('attribute `can_place_ball` is not an object of type `int`')
        self._can_place_ball = can_place_ball 
    
    @max_allowed_bots.setter
    def max_allowed_bots(self, max_allowed_bots: int) -> None:
        if not isinstance(max_allowed_bots, int):
           log.error('attribute `max_allowed_bots` is not an object of type `int`')
        self._max_allowed_bots = max_allowed_bots 
    
    @bot_substitution_intent.setter
    def bot_substitution_intent(self, bot_substitution_intent: bool) -> None:
        if not isinstance(bot_substitution_intent, bool):
           log.error('attribute `bot_substitution_intent` is not an object of type `bool`')
        self._bot_substitution_intent = bot_substitution_intent 
    
    @ball_placement_failures_reached.setter
    def ball_placement_failures_reached(self, ball_placement_failures_reached: bool) -> None:
        if not isinstance(ball_placement_failures_reached, bool):
           log.error('attribute `ball_placement_failures_reached` is not an object of type `bool`')
        self._ball_placement_failures_reached = ball_placement_failures_reached 
    
    @bot_substitution_allowed.setter
    def bot_substitution_allowed(self, bot_substitution_allowed: bool) -> None:
        if not isinstance(bot_substitution_allowed, bool):
           log.error('attribute `bot_substitution_allowed` is not an object of type `bool`')
        self._bot_substitution_allowed = bot_substitution_allowed 
    
    @bot_substitutions_left.setter
    def bot_substitutions_left(self, bot_substitutions_left: int) -> None:
        if not isinstance(bot_substitutions_left, int):
           log.error('attribute `bot_substitutions_left` is not an object of type `int`')
        self._bot_substitutions_left = bot_substitutions_left

    @bot_substitution_time_left.setter
    def bot_substitution_time_left(self, bot_substitution_time_left: int) -> None:
        if not isinstance(bot_substitution_time_left, int):
           log.error('attribute `bot_substitution_time_left` is not an object of type `int`')
        self._bot_substitution_time_left = bot_substitution_time_left

    def __init__(self, **kwargs) -> None:
        for kw in kwargs:
            # log.warn(f"{kw} {kwargs[kw]}")
            setattr(self, kw, kwargs[kw])

    def __repr__(self) -> str:
        string = "\n"
        for k in self.__dict__.keys():
            string += f"\t\t\033[0;33m{k}\033[0m: {repr(self.__dict__[k])}\n"
        return string

class State:
    @property
    def source_identifier(self) -> str:
        return self._source_identifier
    
    @property
    def match_type(self) -> Match:
        return self._match_type

    @property
    def packet_timestamp(self) -> int:
        return self._packet_timestamp
    
    @property
    def stage(self) -> Stage:
        return self._stage
    
    @property
    def stage_time_left(self) -> int:
        return self._stage_time_left

    @property
    def command(self) -> GameControllerCommand:
        return self._command

    @property
    def command_counter(self) -> int:
        return self._command_counter

    @property
    def command_timestamp(self) -> int:
        return self._command_timestamp
    
    @property
    def yellow(self) -> TeamInformation:
        return self._yellow
    
    @property
    def blue(self) -> TeamInformation:
        return self._blue
    
    @property
    def designated_position(self) -> Point:
        return self._designated_position
    
    @property
    def blue_team_on_positive_half(self) -> bool:
        return self._blue_team_on_positive_half
    
    @property
    def next_command(self) -> GameControllerCommand:
        return self._next_command
    
    @property
    def game_events(self) -> Event:
        return self._game_events

    @source_identifier.setter
    def source_identifier(self, source_identifier: str) -> None:
        if not isinstance(source_identifier, str):
           log.error('attribute `source_identifier` is not an object of type `str`')
        self._source_identifier = source_identifier
    
    @match_type.setter
    def match_type(self, match_type: Match) -> None:
        if not isinstance(match_type, Match):
           log.error('attribute `match_type` is not an object of type `Match`')
        self._match_type = match_type
    
    @packet_timestamp.setter
    def packet_timestamp(self, packet_timestamp: int) -> None:
        if not isinstance(packet_timestamp, int):
           log.error('attribute `packet_timestamp` is not an object of type `int`')
        self._packet_timestamp = packet_timestamp

    @stage.setter
    def stage(self, stage: Stage) -> None:
        if not isinstance(stage, Stage):
           log.error('attribute `stage` is not an object of type `Stage`')
        self._stage = stage

    @stage_time_left.setter
    def stage_time_left(self, stage_time_left: int) -> None:
        if not isinstance(stage_time_left, int):
           log.error('attribute `stage_time_left` is not an object of type `int`')
        self._stage_time_left = stage_time_left

    @command.setter
    def command(self, command: GameControllerCommand) -> None:
        if not isinstance(command, GameControllerCommand):
           log.error('attribute `command` is not an object of type `GameControllerCommand`')
        self._command = command

    @command_counter.setter
    def command_counter(self, command_counter: int) -> None:
        if not isinstance(command_counter, int):
           log.error('attribute `command_counter` is not an object of type `float`')
        self._command_counter = command_counter

    @command_timestamp.setter
    def command_timestamp(self, command_timestamp: int) -> None:
        if not isinstance(command_timestamp, int):
           log.error('attribute `command_timestamp` is not an object of type `int`')
        self._command_timestamp = command_timestamp

    @yellow.setter
    def yellow(self, yellow: TeamInformation) -> None:
        if not isinstance(yellow, TeamInformation):
            log.error("attribute `yellow` is not an object of type `TeamInformation`")
        self._yellow = yellow

    @blue.setter
    def blue(self, blue: TeamInformation) -> None:
        if not isinstance(blue, TeamInformation):
            log.error("attribute `blue` is not an object of type `TeamInformation`")
        self._blue = blue

    @designated_position.setter
    def designated_position(self, designated_position: Point) -> None:
        if not isinstance(designated_position, Point):
            log.error("attribute `designated_position` is not an object of type `Point`")
        self._designated_position = designated_position

    @blue_team_on_positive_half.setter
    def blue_team_on_positive_half(self, blue_team_on_positive_half: bool) -> None:
        if not isinstance(blue_team_on_positive_half, bool):
            log.error("attribute `blue_team_on_positive_half` is not an object of type `bool`")
        self._blue_team_on_positive_half = blue_team_on_positive_half
    
    @next_command.setter
    def next_command(self, next_command: GameControllerCommand) -> None:
        if not isinstance(next_command, GameControllerCommand):
            log.error("attribute `next_command` is not an object of type `GameControllerCommand`")
        self._next_command = next_command

    @game_events.setter
    def game_events(self, game_events: Event) -> None:
        if not isinstance(game_events, Event):
            log.error("attribute `next_command` is not an object of type `Event`")
        self._game_events = game_events

    def __setattr__(self, name: object, value: object) -> None:
        match name:
            case 'match_type':
                value = Match[value]
            case 'stage': 
                value = Stage[value]
            case 'command' | 'next_command':
                # log.warn(f"{name=} {value=}")
                value = GameControllerCommand[value]
            case 'designated_position':
                x = value['x']
                y = value['y']

                value = Point()
                value.x = x
                value.y = y
            case 'yellow' | 'blue':
                value = TeamInformation(**value)
            case 'game_events':
                value = EventFactory()(value)
            
        object.__setattr__(self, name, value)

    def __init__(self, **kwargs) -> None:
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])

    def __repr__(self) -> str:
        string = ""
        for k in self.__dict__.keys():
            string += f"\t\033[0;33m{k}\033[0m: {repr(self.__dict__[k])}\n"
        return string

class States:
    def __init__(self) -> None:
        self._states = list()

    def register_next_state(self, **kwargs) -> None:
        state = State(**kwargs)
        self._states.append(state)

    def __len__(self) -> int:
        return len(self._states)
    
    def __str__(self):
        ...

    def __getitem__(self, index: int):
        if isinstance(index, int):
            try:
                return self._states[index]
            except IndexError as e:
                log.error(e)

    def __contains__(self, index: int):
        if not isinstance(index, int):
           log.error('attribute `index` is not an object of type `int`')
    
        if index > len(self):
            return False
        if index < 0:
            return False
        return True

    @property
    def get_current_state(self) -> State:
        if len(self._states) == 0:
            raise ValueError("GameState.py: object 'States' is empty")
        return self._states[-1]

if __name__ == "__main__":
    ...
