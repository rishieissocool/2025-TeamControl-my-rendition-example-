import numpy as np
import numpy.typing as npt
from TeamControl.Model.field import *
from TeamControl.Model.frame import *
import TeamControl.Model as model
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class World:
    """
    World Model aka wm
    Description : 
        This class contains data extracted from Vision world. (Either Simulation or Vision-ssl). 
        
        The model will first compare whether the data is type 'detection' or 'geometry'. 
        
        -- Detection --
        If the data is detection, the model will check the 'Frame Number'.
            if it is an existing one, it will reuse the frame and update new data. 
            if it is a NEW one, it will initiate a new Frame object
            
        -- Geometry --
        if the data is geometry, the model will create an Object of the class : Field
        *since this is a static data, it does not require constant update*
        
    Params : 
        --Booleans--
        isYellow (bool) : is Our Team Yellow
        isPositive (bool) : is Our Team on x-Positive side
        is_detection_updated (bool) : has detection been updated yet
         
        --Integers--
        cframe (int) : current frame number 
        # gap (int) : the gap number between frames stored Please leave at Default: 0. 
        max_frames (int) : max number of frames to be stored in history 
        max_cameras (int) : max number of cameras active
        
        --List--
        frames (list): list of frames history
        
        --Object--
        field (Field): object of Field Class
        
    """
    def __init__(self, isYellow : bool, isPositive : bool, gap : int=0, max_frames : int=3, max_cameras : int=1):
        """world Model Initiate 

        Args:
            isYellow (bool): Boolean for Is your Team YELLOW.
            isPositive (bool): Boolean for Is your Team On X positive side.
            gap (int, optional): Number of frames to skip. Defaults to 0.
            max_frames (int, optional): Number of max frames to store in history. Defaults to 5.
            max_cameras (int, optional): Number of active Cameras. Defaults to 4.
        
        Params : 
            is_detection_updated (bool): variable used to identify whether the current model has a new frame fully updated. 
                                         Should always set to false unless the frame has been fully updated.
            frames (list): list of Frame objects.
            field (Field): The field object for geometry of the map.
        """
        self.isYellow:bool = isYellow
        self.isPositive:bool = isPositive
        self.cframe:int = None
        self.gap:int = gap
        self.max_frames:int = max_frames
        self.max_cameras:int = max_cameras
        self.is_detection_updated:bool = False
        self.frames:list[Frame] = list() 
        self.field:Field = None # geometry 
        log.info(f"World Model has been initialized {str(self)}")

### --- UPDATE --- ###
    def update(self, data) -> bool | None:
        if data is None:
            return False
        try:
            # if the data received has field : detection
            if data.HasField("detection"):
                debug_print("Updating Detection")
                # updates the detection data in world model
                self.__update_detection(data.detection)
                # returns whether the detection model is updated
                            
            # if the data received has field : geometry
            if data.HasField("geometry") :
                # if our geometry is not set 
                if self.field is None:
                    # updates our geometry
                    self.__update_geometry(data.geometry)
                    log.info("Geometry has been set")
                    # otherwise leave it . 
        except ValueError:
            log.info("new data : \n" ,data)
        return self.is_detection_updated
            

    
    def __update_detection(self,detection) -> None:
        """Update detection (frame)
        This func. creates / updates frame objects with new data recv. from vision world
        Args:
            detection (data): decoded protobuf data from vision world.
        
        Params: 
            new_frame (Frame): the new frame object to store data about this frame
            curret_frame (Frame): the Current Frame that you want to update the data in         
        """
        # print(detection)
        #if current newest frame number is smaller than the new frame number received
        if self.cframe is None or (self.cframe + self.gap < detection.frame_number):
            self.is_detection_updated = False
            # updates current frame number as detection frame number
            self.cframe = detection.frame_number
            #initiate new frame object
            new_frame = Frame(detection)
            # debug_print(f"frame is added")
            # adds frame onto list of histroy frames
            self.frames.append(new_frame)
            # if the length of frames exceeds 'max_frames', remove the first frame.
            if (len(self.frames)>self.max_frames):
                self.frames.pop(0)
            
            # if self.max_cameras-1 == 0:
            #     self.is_detection_updated = True
            #     return self.is_detection_updated

                
        # if the current newest frame number is the frame number received
        elif self.cframe == detection.frame_number:
            #retrieve current newest frame
            current_frame:Frame = self.frames[-1]
            #update frame object with new data
            current_frame.update(detection)
            #update frame object in list (frames)
            self.frames[-1] = current_frame
        if not self.is_detection_updated and detection.camera_id == self.max_cameras-1:
            self.is_detection_updated = True
            # log.info(f"{self.cframe=} is updated")
        else:
            self.is_detection_updated = False
        
        

    def __update_geometry(self,geometry):
        """_summary_
            Retrieves geometry data about the field and stores in the world_model.
        Args:
            geometry (data): data about field
        """
        self.field = Field(geometry.field)
       
    def update_team_side(self,isYellow:bool,isPositive:bool):
        self.isYellow : bool = isYellow
        self.isPositive : bool = isPositive

### --- Get --- ###
    def get_last_frame(self, i=0) -> Frame:
        """get last frame
        Get's the last frame from history of frames

        Args:
            i (int, optional): index number counted from the back. Defaults to 0 (latest).

        Returns:
            Frame: corresponding frame as requested
        """
      
        if i in range(len(self.frames)):
            i = i+1
            frame = self.frames[-i]
            if isinstance(frame,Frame):
                return frame
            else:
                log.error("No Frame object at -",i)
                return None
            
    
    def get_team_color(self,ourTeam:bool) -> bool:
        """get team color
        returns our or enemy team color in terms of 'isYellow' boolean.

        Args:
            ourTeam (bool): Are you trying to get our Team's color ? True(Y) or False(N).

        Returns:
            bool: team color requested in the form of 'isYellow'.
        """
        if ourTeam is True:
            return self.isYellow
        elif ourTeam is False:
            return not(self.isYellow)
    
    def get_robot(self,isYellow:bool,robot_id:int, format:int, hist:bool=False):
        history = list()
        if robot_id is None or not isinstance(robot_id,int):
            raise ("robot id must be an INT")
        
        for i in range(len(self.frames)):
            # gets latest frame object
            frame : Frame = self.get_last_frame(i)
            if frame is not None :
                robot = frame.has_id(isYellow=isYellow,robot_id=robot_id)
                if robot is not None:
                    result = frame.get_robot(isYellow=isYellow,robot_id=robot_id,format=format)
                    if hist is False:
                        # print(result)
                        return result
                    elif hist is True: 
                        history.append(result)
                        log.info(f"result added robot:{robot_id}")
                else:
                    log.warning(f"No such robot @{frame=},team:{isYellow=}, robot: {robot_id=}")
            else:
                log.warning(f"No Frame @ {frame=}")
                
        if hist is True : 
            return history
        else:
            return None
    def get_team(self,isYellow:bool,format:int,hist:bool=False):
        history = list()
        for i in range(len(self.frames)):
            # gets latest frame object
            frame : Frame = self.get_last_frame(i)
            if isinstance(frame,Frame) :
                return frame.get_team_robots(isYellow,format)
        if hist is True : 
            return history
        else:
            return []
    
    
    def get_our_ids(self)-> list[int]:
        our_ids = (self.get_team(isYellow=self.get_team_color(ourTeam=True),format=Robot.ID))
        if our_ids is None:
            return []
        return our_ids
    

    def get_enemy_ids(self) -> list[int]:
        enemy_ids = (self.get_team(isYellow=self.get_team_color(ourTeam=False),format=Robot.ID))
        if enemy_ids is None:
            return []
        return enemy_ids
    
    def get_our_robot(self, robot_id: int, format: int=Robot.CORDS, hist: bool=False) -> tuple[float,float,float]:
        # loop for frames to look for latest robot position known
        ourTeam = self.get_team_color(ourTeam=True)
        if robot_id is None:
            return self.get_team(ourTeam,format,hist)
        else:
            return self.get_robot(ourTeam,robot_id,format,hist)

    def get_enemy_robot(self, robot_id: int, format: int=Robot.CORDS, hist: bool=False) -> tuple[float,float,float]:
        enemyTeam = self.get_team_color(ourTeam=False)
        if robot_id is None:
            return self.get_team(enemyTeam,format,hist)
        else:
            return self.get_robot(enemyTeam,robot_id,format,hist)


    def get_ball(self,hist=False) -> tuple[float,float]|npt.ArrayLike:
        """Get The Ball Data: 
        This can give you either a single [ballx, bally] or a list of them.
        To do so, toggle 
        hist = True -> returns a list, 
        hist = False -> returns a single one

        Args:
            hist (bool, optional): toggle between list or a single tuple being retrieved. Defaults to False.

        Returns:
            tuple[float,float]|np.array|None: either you get a single ball data retruned, or a list of them or nothing.
        """
        # loop for frames to look for latest robot position known
        if hist is True:
            ball_hist = np.empty(len(self.frames),dtype='f,f')
        for i in range(len(self.frames)):
            # gets latest frame object
            frame:Frame = self.get_last_frame(i)
            if isinstance(frame,Frame) and frame is not None:
                # gets ball position from frame object
                ball_pos : tuple[float,float] = frame.get_ball()
                # if ball position is found
                if ball_pos is not None: 
                    # debug_print(f"Ball found at {ball_pos}")
                    if hist is True:
                        # appends ball position into np. array
                        ball_hist[i] = ball_pos
                    else:
                        # otherwise returns this ball position 
                        return ball_pos
                else:
                    log.info(f"No ball found at frame {frame.id=}")
            else:
                log.info(f"No Frame found at -{i}")
        if hist is True:
            log.info(f"ball_hist=")
            return ball_hist
        else:
            # otherwise no ball found
            log.warning(f"There's no ball ??")
            return None

    def __repr__(self):
        """__repr__ in depth description of World Model

        Returns:
            str: log info of 99% of World Model
        """
        return f'''
World Model 
Current Frame : {self.cframe}
has Frame been fully Updated ? : {self.is_detection_updated}
has {len(self.frames)} frames, maximum : {self.max_frames}
has Cameras : {self.max_cameras}

Our Team Color : {self.isYellow=} , {self.isPositive=}

Latest Data : 
Our Team Robots : 
ACTIVE : {len(self.get_our_ids())} ID: {self.get_our_ids()}
POS : {self.get_our_robot(None)}

Enemy Team Robots : 
ACTIVE : {len(self.get_enemy_ids())} ID: {self.get_enemy_ids()}
POS : {self.get_enemy_robot(None)}

BALL Located : 
{self.get_ball()}


Current list of Frame History : {len(self.frames)} frames available, maximum : {self.max_frames}

    '''
    
    def __str__(self):
        """__str__ Returns a simple Representation of World Model.

        Returns:
            str: simple form of output to check for the world model basics.
        """
        return f'is Our Team Yellow ? {self.isYellow} , field is Positive Half ? {self.isPositive}. World Model has {len(self.frames)} frames, has geometry been initialized ? {self.field!=None}'
    
# Field data : 
# {self.field}
# {self.frames}
