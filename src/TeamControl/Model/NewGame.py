from TeamControl.Model.GameState import GameControllerCommand, Stage, Team
from TeamControl.Model.frame import Robot
import logging
import matplotlib.pyplot as plt
import numpy as np

log = logging.getLogger()
log.setLevel(logging.NOTSET)

class graphics:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.yellow_x = []
        self.yellow_y = []
        self.blue_x = []
        self.blue_y = []
        self.ball_x = []
        self.ball_y = []

        self.world_model = None
    
    def update_plot(self):
        if self.world_model is None:
            return 
    
        self.yellow_x = []
        self.yellow_y = []
        self.yellow_ox = []
        self.yellow_oy = []
        self.ax.clear()

        for x, y, o in self.world_model.get_team(isYellow=True, format=Robot.CORDS):

            self.yellow_x.append(x)
            self.yellow_y.append(y)
            self.yellow_ox.append(x)
            self.yellow_ox.append(x - 400)
            self.yellow_oy.append(y)
            self.yellow_oy.append(y + 400*np.sin(o))
            self.ax.plot(self.yellow_ox, self.yellow_oy, ls='-', color='y')
            self.yellow_ox = []
            self.yellow_oy = []

        self.blue_x = []
        self.blue_y = []
        self.blue_ox = []
        self.blue_oy = []
        for x, y, o in self.world_model.get_team(isYellow=False, format=Robot.CORDS):

            self.blue_x.append(x)
            self.blue_y.append(y)
            self.blue_ox.append(x)
            self.blue_ox.append(x + 400)
            self.blue_oy.append(y)
            self.blue_oy.append(y + 400*-np.sin(o))
            self.ax.plot(self.blue_ox, self.blue_oy, ls='-', color='b')
            self.blue_ox = []
            self.blue_oy = []

        try:
            x, y = self.world_model.get_ball()
            self.ball_x = [x]
            self.ball_y = [y]
            self.ax.scatter(self.ball_x, self.ball_y, color='r')
        except TypeError as err:
            log.critical(err)

        self.ax.scatter(self.yellow_x, self.yellow_y, color='y', alpha=0.5)
        # self.ax.plot(self.yellow_ox, self.yellow_oy, ls='-', alpha=0.3)
        self.ax.scatter(self.blue_x, self.blue_y, color='b', alpha=0.5)
        # self.ax.plot(self.blue_ox, self.blue_oy, ls='-', alpha=0.3)

        right_x = 6000
        left_x = -6000

        right_y = 4000
        left_y = -4000
        self.ax.set_xlim(left_x, right_x)
        self.ax.set_ylim(left_y, right_y)
        self.fig.canvas.draw()

        plt.show()
        plt.pause(0.01)
    
    @property
    def world_model(self):
        return self._world_model

    @world_model.setter
    def world_model(self, world_model):
        self._world_model = world_model

class tc:
    def __init__(self, namespace, new_state_q, send_to_robot_q):
        self._curr_gc_stage = None
        self.last_gc_stage_transition = None
        self.states = new_state_q
        self._world_model = None
        self._tc_gc_state_controller = _tc_gc_state_controller(self.world_model, new_state_q, send_to_robot_q)

        self.graphics = graphics()

    @property
    def world_model(self):
        return self._world_model

    @world_model.setter
    def world_model(self, world_model):
        self._world_model = world_model

    @property
    def curr_gc_stage(self):
        return self._curr_gc_stage

    @curr_gc_stage.setter
    def curr_gc_stage(self, curr_gc_stage):
        if not curr_gc_stage is self._curr_gc_stage:
            log.warn(f'ssl_vision_wrapper_pb2 transition: {self._curr_gc_stage} => {self.curr_gc_stage}')
            self._curr_gc_stage = curr_gc_stage
            self.gc_stage_transition = True

    @property
    def get_stage_callable(self):
        if self.curr_gc_stage is None:
            log.error(f"self._curr_gc_stage is None")
            return None

        foo = {
            Stage.NORMAL_FIRST_HALF_PRE: self.normal_first_half_pre,
            Stage.NORMAL_FIRST_HALF: self.normal_first_half,
            Stage.NORMAL_HALF_TIME: self.normal_half_time,
            Stage.NORMAL_SECOND_HALF_PRE: self.normal_second_half_pre,
            Stage.NORMAL_SECOND_HALF: self.normal_second_half,
            Stage.EXTRA_TIME_BREAK: self.extra_time_break,
            Stage.EXTRA_FIRST_HALF_PRE: self.extra_first_half_pre,
            Stage.EXTRA_FIRST_HALF: self.extra_first_half,
            Stage.EXTRA_HALF_TIME: self.extra_half_time,
            Stage.EXTRA_SECOND_HALF_PRE: self.extra_second_half_pre,
            Stage.EXTRA_SECOND_HALF: self.extra_second_half,
            Stage.PENALTY_SHOOTOUT_BREAK: self.penalty_shootout_break,
            Stage.PENALTY_SHOOTOUT: self.penalty_shootout,
            Stage.POST_GAME: self.post_game,
        }
        return foo.get(self.curr_gc_stage)

    def normal_first_half_pre(self):
        # log.info(f'{self.normal_first_half_pre.__name__}() called')
        self._normal_first_half_pre()

    def normal_first_half(self):
        # log.info(f'{self.normal_first_half.__name__}() called')
        self._normal_first_half()

    def normal_half_time(self):
        # log.info(f'{self.normal_half_time.__name__}() called')
        self._normal_half_time()

    def normal_second_half_pre(self):
        # log.info(f'{self.normal_second_half_pre.__name__}() called')
        self._normal_second_half_pre()

    def normal_second_half(self):
        # log.info(f'{self.normal_second_half.__name__}() called')
        self._normal_second_half()

    def extra_time_break(self):
        # log.info(f'{self.extra_time_break.__name__}() called')
        self._extra_time_break()

    def extra_first_half_pre(self):
        # log.info(f'{self.extra_first_half_pre.__name__}() called')
        self._extra_first_half_pre()

    def extra_first_half(self):
        # log.info(f'{self.extra_first_half.__name__}() called')
        self._extra_first_half()

    def extra_half_time(self):
        # log.info(f'{self.extra_first_half.__name__}() called')
        self._extra_half_time()

    def extra_second_half_pre(self):
        # log.info(f'{self.extra_second_half_pre.__name__}() called')
        self._extra_second_half_pre()

    def extra_second_half(self):
        # log.info(f'{self.extra_second_half.__name__}() called')
        self._extra_second_half()

    def penalty_shootout_break(self):
        # log.info(f'{self.penalty_shootout_break.__name__}() called')
        self._penalty_shooutout_break()

    def penalty_shootout(self):
        # log.info(f'{self.penalty_shootout.__name__}() called')
        self._penalty_shootout()

    def post_game(self):
        # log.info(f'{self.post_game.__name__}() called')
        self._post_game()

    def run(self):
        self.graphics.world_model = self.world_model
        self.graphics.update_plot()
        if not self.states.empty():
            new_state = self.states.get()
            # log.info(f'{new_state}')
            # log.info(f"{self.world_model}")
            self.curr_gc_stage = new_state.stage
            if self.gc_stage_transition:
                self.get_stage_callable()
                self.gc_stage_transition = False

            self.curr_gc_cmd = new_state.command
            self._tc_gc_state_controller.world_model = self.world_model
            # print(self._tc_gc_state_controller.world_model)
            self._tc_gc_state_controller.curr_gc_cmd = self.curr_gc_cmd
            if self._tc_gc_state_controller.new_gc_cmd:
                self._tc_gc_state_controller.gc_transition_state_func()
                self.new_gc_cmd = False
                return
            
            if not self._tc_gc_state_controller.ready_for_game_state:
                self._tc_gc_state_controller.gc_transition_state_func()
                return

            self._tc_gc_state_controller.gc_state_cmd()


class _tc_gc_state_controller:
    def __init__(self, world_model, new_state_q, send_to_robot_q):
        self.world_model = world_model
        self.states = new_state_q
        self.send_to_robot_q = send_to_robot_q
        self.curr_gc_state = None
        self._curr_gc_cmd = None
        self._prev_gc_cmd = None
        # self.is_yellow = world_model.isYellow
        self.ready_for_game_state = False

    @property
    def curr_gc_cmd(self):
        return self._curr_gc_cmd

    @curr_gc_cmd.setter
    def curr_gc_cmd(self, curr_gc_cmd):
        if not self._curr_gc_cmd is curr_gc_cmd:
            log.warn(f'ssl_gc_referee_message_pb2 transition: {self._curr_gc_cmd} => {curr_gc_cmd}')
            self._curr_gc_cmd = curr_gc_cmd
            self.new_gc_cmd = True

    @property
    def world_model(self):
        return self._world_model
    
    @world_model.setter
    def world_model(self, world_model):
        self._world_model = world_model   
    
    @property
    def prev_gc_cmd(self):
        return self._prev_gc_cmd

    @property
    def our_team_colour(self):
        if self.world_model is None:
            return
        if self.world_model.isYellow:
            return Team.YELLOW
        return Team.BLUE

    @property
    def gc_transition_state_func(self):
        if self.curr_gc_cmd is None:
            log.error(f"self._curr_gc_cmd is None")
            return None
        foo = {
            GameControllerCommand.HALT: self.halt,
            GameControllerCommand.STOP: self.stop,
            GameControllerCommand.NORMAL_START: self.normal_start,
            GameControllerCommand.FORCE_START: self.force_start,
            GameControllerCommand.PREPARE_KICKOFF_YELLOW: self.prepare_kickoff_yellow,
            GameControllerCommand.PREPARE_KICKOFF_BLUE: self.prepare_kickoff_blue,
            GameControllerCommand.PREPARE_PENALTY_YELLOW: self.prepare_penalty_yellow,
            GameControllerCommand.PREPARE_PENALTY_BLUE: self.prepare_penatly_blue,
            GameControllerCommand.DIRECT_FREE_YELLOW: self.direct_free_yellow,
            GameControllerCommand.DIRECT_FREE_BLUE: self.direct_free_blue,
            GameControllerCommand.INDIRECT_FREE_YELLOW: self.indirect_free_yellow,
            GameControllerCommand.INDIRECT_FREE_BLUE: self.indirect_free_blue,
            GameControllerCommand.TIMEOUT_YELLOW: self.timeout_yellow,
            GameControllerCommand.TIMEOUT_BLUE: self.timeout_blue,
            GameControllerCommand.GOAL_YELLOW: self.goal_yellow,
            GameControllerCommand.GOAL_BLUE: self.goal_blue,
            GameControllerCommand.BALL_PLACEMENT_YELLOW: self.ball_placement_yellow,
            GameControllerCommand.BALL_PLACEMENT_BLUE: self.ball_placement_blue,
            GameControllerCommand.UNKNOWN_COMMAND: self.unknown_command,
        }
        func = foo.get(self.curr_gc_cmd)
        return func

    def halt(self):
        # log.info(f'{self.halt.__name__}() called')
        self._halt()

    def stop(self):
        # log.info(f'{self.stop.__name__}() called')
        self._stop()

    def prepare_kickoff_yellow(self):
        # log.info(f'{self.prepare_kickoff_yellow.__name__}() called')
        if self.our_team_colour == Team.YELLOW:
            self._prepare_kickoff_yellow()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def prepare_kickoff_blue(self):
        # log.info(f'{self.prepare_kickoff_blue.__name__}() called')
        if self.our_team_colour == Team.BLUE:
            self._prepare_kickoff_blue()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def normal_start(self):
        # log.info(f'{self.normal_start.__name__}() called')
        self._normal_start()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.running()

    def force_start(self):
        # log.info(f'{self.force_start.__name__}() called')
        self._force_start()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.running()

    def prepare_kickoff_yellow(self):
        # log.info(f'{self.prepare_kickoff_yellow.__name__}() called')
        if self.our_team_colour == Team.YELLOW:
            self.prepare_kickoff_yellow()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def prepare_kickoff_blue(self):
        # log.info(f'{self.prepare_kickoff_blue.__name__}() called')
        if self.our_team_colour == Team.BLUE:
            self._prepare_kickoff_blue()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def prepare_penalty_yellow(self):
        if self.our_team_colour == Team.YELLOW:
            self._prepare_penalty_yellow()
        # log.info(f'{self.prepare_penalty_yellow.__name__}() called')
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def prepare_penatly_blue(self):
        if self.our_team_colour == Team.BLUE:
            self._prepare_penatly_blue()
        # log.info(f'{self.prepare_penatly_blue.__name__}() called')
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def direct_free_yellow(self):
        # log.info(f'{self.direct_free_yellow.__name__}() called')
        if self.our_team_colour == Team.YELLOW:
            self._direct_free_yellow()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def direct_free_blue(self):
        # log.info(f'{self.direct_free_blue.__name__}() called')
        if self.our_team_colour == Team.BLUE:
            self._direct_free_blue()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def indirect_free_yellow(self):
        # log.info(f'{self.indirect_free_yellow.__name__}() called')
        if self.our_team_colour == Team.YELLOW:
            self._indirect_free_yellow()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def indirect_free_blue(self):
        # log.info(f'{self.indirect_free_blue.__name__}() called')
        if self.our_team_colour == Team.BLUE:
            self._indirect_free_blue()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def timeout_yellow(self):
        # log.info(f'{self.timeout_yellow.__name__}() called')
        self._timeout_yellow()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.halted()

    def timeout_blue(self):
        # log.info(f'{self.timeout_blue.__name__}() called')
        self._timeout_blue()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.halted()

    def goal_yellow(self):
        # log.info(f'{self.goal_yellow.__name__}() called')
        self._goal_yellow()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.halted()

    def goal_blue(self):
        # log.info(f'{self.goal_blue.__name__}() called')
        self._goal_blue()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.halted()

    def ball_placement_yellow(self):
        # log.info(f'{self.ball_placement_yellow.__name__}() called')
        if self.our_team_colour == Team.YELLOW:
            self._ball_placement_yellow()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def ball_placement_blue(self):
        # log.info(f'{self.ball_placement_blue.__name__}() called')
        if self.our_team_colour == Team.BLUE:
            self._ball_placement_blue()
        if self.ready_for_game_state:
            self.gc_state_cmd = self.stopped()

    def unknown_command(self):
        """
         >>> from TeamControl.RobotBehaviour.behaviour import RobotMovement
         >>> ball = self.world_model.get_ball()
         >>> frame = self.world_model.get_last_frame()
         >>> robot = frame.get_robot(isYellow=True, robot_id=5, format=Robot.CORDS)
         >>> log.critical(robot)

         >>> r_x = robot[0]
         >>> r_y = robot[1]
         >>> r_w = robot[2]

         >>> log.warn(f"{r_x}, {r_y}, {r_w}")
         >>> vx, vy, w = RobotMovement.velocity_to_target((r_x, r_y, r_w), target=(0, 0), stop_threshold=700)
         >>> vx *= 100
         >>> vy *= 100
         >>> new_action = Action(5, vx, vy, w)
         >>> self.send_to_robot_q.put(new_action)
        """
        # log.info(f'{self.unknown_command.__name__}() called')

    def running(self):
        log.info(f"{self.running.__name__}() called")
        self._run()

    def stopped(self):
        log.info(f"{self.stopped.__name__}() called")
        self._stop()

    def halted(self):
        log.info(f"{self.halted.__name__}() called")
        self._halt()
