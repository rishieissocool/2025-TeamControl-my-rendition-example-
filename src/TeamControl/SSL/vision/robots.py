from TeamControl.voronoi_planner.obstacle import Obstacle

import numpy as np


class Robot:
    """
    Represents an individual robot detected on the field. from (SSL.proto2.detection)
    
    Attributes:
        isYellow (bool): Whether the robot belongs to the yellow team.
        id (int): The robot's unique ID (0–15).
        c (float): Confidence level of the detection.
        x (float): X position in world coordinates.
        y (float): Y position in world coordinates.
        o (float): Orientation in radians.
        px (float): X position in pixel coordinates (image space).
        py (float): Y position in pixel coordinates (image space).
    """
    def __init__(self,robot_data,isYellow:bool) -> object:
        self.isYellow : bool = isYellow
        self.id : int = robot_data.robot_id
        self.c : float = robot_data.confidence
        self.x : float = robot_data.x
        self.y : float = robot_data.y
        self.o : float = robot_data.orientation
        self.px : float = robot_data.pixel_x
        self.py : float = robot_data.pixel_y
        
    @property
    def position(self) -> np.dtype:
        """
        Returns the robot's position and orientation as a NumPy array.

        Returns:
            np.ndarray: [x, y, o] in float32.
        """
        return np.array([self.x, self.y, self.o], dtype=np.float32)
    
    # def __lt__(self,other):
    #     return self.id < other.id
    
    @property
    def obstacle(self) -> Obstacle:
        """
        Returns a Voronoi-compatible obstacle representation of this robot.

        Returns:
            Obstacle: Circular obstacle for collision planning.
        """
        # buffer = 250
        # top_left= [self.x-buffer, self.y+buffer]
        # bottom_right= [self.x+buffer, self.y-buffer]
        # return Obstacle(top_left, bottom_right)
    
        return Obstacle(point=(self.x,self.y),
                        radius=90,
                        unum=self.id,
                        isYellow=self.isYellow)    
    
    def __repr__(self):
        color = 'Yellow' if self.isYellow else 'Blue'
        return (
        f"Team: {color}, Robot ID: {self.id}, Confidence: {self.c:.2f}\n"
        f"Position: {self.position} | Pixel: ({self.px}, {self.py})\n"
        f"Obstacle: {self.obstacle}"
    )
        

class Team ():
    """
    Represents a team of robots (yellow or blue) using a fixed-size array of robot instances.
    
    Attributes:
        isYellow (bool): Indicates if this team is yellow.
    """
    def __init__(self,team_robots:list, team_is_yellow:bool):
        """
        Initializes a Team instance using a list of raw protobuf robot data.

        Args:
            team_robots (list): List of protobuf robot objects (e.g., SSL_DetectionRobot).
            team_is_yellow (bool): True if the team is yellow.
        """
        self._robots : np.ndarray=np.zeros(16,dtype=object)
        self.isYellow : bool= team_is_yellow
        self.robots = team_robots #sets and updates the value
    

    @property
    def robots(self):
        """
        Returns:
            np.ndarray: Array of Robot objects or empty slots.
        """
        return self._robots
    
    @robots.setter
    def robots(self,team_robots):
        """Populates internal robot array from raw protobuf robot data."""
        robots = [Robot(data, self.isYellow) for data in team_robots]
        for r in robots:
            robot_id = int(r.id)
            if 0 <= robot_id < 16:
                self._robots[robot_id] = r
            else:
                raise ValueError(f"Invalid robot ID: {robot_id} (must be 0–15)")

    
    @property
    def num_robots(self) -> int:
        return sum(isinstance(r, Robot) for r in self._robots)
        
    @property
    def active(self) -> list:
        return [i for i, robot in enumerate(self._robots) if isinstance(robot, Robot)]    
    
    
    def merge(self, other_team: "Team"):
        if not isinstance(other_team, Team):
            raise TypeError("merge() expects a Team instance, use add_robots for list instead")
        if self.isYellow != other_team.isYellow:
            raise ValueError(f"Cannot merge teams of different colors: {self.isYellow=}, {other_team.isYellow=}")
        
        self.add_robots([r for r in other_team.robots if isinstance(r, Robot)])

    def add_robots(self,team_robots:list):
        for new_robot in team_robots:
            robot_id = int(new_robot.robot_id)
            if robot_id in self:
                print(f"robot is found with data {self[robot_id]}")
            if 0 <= robot_id < 16:
                self._robots[robot_id] = new_robot if isinstance(new_robot, Robot) else Robot(isYellow=self.isYellow, robot_data=new_robot)
            else:
                raise ValueError(f"Invalid robot ID: {robot_id} (must be 0–15)")
        
    def __len__(self):
        return self.num_robots
    
    def __iter__(self):
        return (robot for robot in self._robots if isinstance(robot, Robot))
    
    def __contains__(self, robot_id: int):
        return isinstance(self._robots[robot_id], Robot)
    
    def __getitem__(self,key:int) -> Robot :
        if 0 <= key < 16:
            return self._robots[key]
        raise IndexError("Robot ID out of valid range (0–15)")

    def __repr__(self):
        return f"{self.isYellow=} : {self.num_robots=} \n {self.active=}"
    
    def get_robot(self, robot_id: int) -> Robot | None:
        if 0 <= robot_id < 16:
            return self._robots[robot_id] if isinstance(self._robots[robot_id], Robot) else None
        return None

if __name__ =="__main__" :
    new_team = Team([],True)
    print(new_team)