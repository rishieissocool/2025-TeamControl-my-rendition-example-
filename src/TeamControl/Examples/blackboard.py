# keeps the current state of the world and the decisions made by the team control
import logging
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional, List
import time

#robot data state 
@dataclass
class BBState:
    # world snapshots
    ball_position: Optional[Tuple[float, float]] = None
    ball_timestamp: float = 0.0
    robots: list = field(default_factory=list)               
    field_size: Tuple[int, int] = (9000, 6000)
    us_yellow: bool = True
    us_positive: bool = True

    # inference
    nearest_robot: Optional[object] = None
    nearest_order: List[object] = field(default_factory=list)

    # goalie
    goal_threat: bool = False
    goalie_save_position: Optional[Tuple[float, float]] = None

    # referee
    gc_command: Optional[object] = None
    gc_stage: Optional[object] = None

    # roles (updated every tick)
    # robot_id: 'GOALIE'|'STRIKER'|'WINGER'|'DEFENDER'|'IDLE'
    roles: Dict[int, str] = field(default_factory=dict)      

    # planner outputs 
    waypoints: Dict[int, List[Tuple[float, float]]] = field(default_factory=dict)

    # tick meta
    tick_ts: float = 0.0

def bb() -> "BBState":
    import py_trees
    board = py_trees.blackboard.Blackboard()
    if not hasattr(board, "state"):
        board.state = BBState()
    return board.state