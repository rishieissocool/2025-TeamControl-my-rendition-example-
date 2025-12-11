import time
import numpy as np

from TeamControl.voronoi_planner.planner import VoronoiPlanner
from TeamControl.world.model import WorldModel as wm
from TeamControl.robot.Movement import RobotMovement
from TeamControl.network.robot_command import RobotCommand


class PathPlanner:
    CLEARANCE = 100
    d0 = 1000
    N = 100

    def __init__(self, world_model: wm, planner_q):
        self.isYellow = True
        self.version = 0
        self.wm = world_model
        field_x, field_y = (9000, 6000)
        self.p = VoronoiPlanner(xsize=field_x, ysize=field_y)
        self.output_q = planner_q

    def check_wm_update(self):
        self.isYellow = (
            self.wm.us_yellow() if hasattr(self.wm, "us_yellow") else self.isYellow
        )

        new_version = self.wm.get_version()
        if self.version <= new_version:
            self.version = new_version
            self.frame = self.wm.get_latest_frame()
            return True
        return False

    def running(self):
        robot_id = 1
        while True:
            is_updated = self.check_wm_update()
            if is_updated and self.frame is not None:
                robot_pos = self.frame.get_yellow_robots(
                    isYellow=self.isYellow, robot_id=robot_id
                ).position
                target_pos = self.frame.ball.position

                waypoints: list = self.pathplanning(
                    robot_id=robot_id, target_pos=target_pos
                )

                point = waypoints[0][1] if len(waypoints[0]) > 1 else None

                print("Robot pos:", robot_pos, "Next:", point)

                vx, vy, w = RobotMovement.velocity_to_target(robot_pos, point)
                command = RobotCommand(robot_id, vx, vy, 0, 0, 0)
                runtime = 1
                self.output_q.put((command, runtime))

    def pathplanning(self, robot_id, target_pos):
        start_pos = [
            self.frame.get_yellow_robots(
                isYellow=self.isYellow, robot_id=robot_id
            ).xy_pos
        ]

        our_robot_obs = [
            r.obstacle
            for r in self.frame.get_all_in_team_except(
                isYellow=self.isYellow, exclude=[5]
            )
        ]
        enemy_robot_obs = [
            r.obstacle
            for r in self.frame.get_all_in_team_except(
                isYellow=not self.isYellow, exclude=[5]
            )
        ]
        all_obstacles = our_robot_obs + enemy_robot_obs

        goals = [target_pos]
        print("number of Obstacles:", len(all_obstacles))

        start_time = time.time()

        self.p.update_obstacles(all_obstacles)

        waypoints = self.p.generate_waypoints(our_robot_obs, goals, self.d0)
        simplified_paths = []
        for i, (start, wp, goal) in enumerate(zip(our_robot_obs, waypoints, goals)):
            full_path = [start.centre()] + wp
            simple = self.p.simplify(full_path, self.CLEARANCE, [start.unum()])
            goal_is_safe = all(
                not obs.is_point_inside(goal) for obs in all_obstacles
            )

            if goal_is_safe and not np.allclose(simple[-1], goal):
                simple.append(goal)

            simplified_paths.append(simple)

        end_time = time.time()
        excution_time = end_time - start_time
        print(f"{excution_time=}")

        return simplified_paths


def run_planner(world_model: wm, planner_q):
    planner = PathPlanner(world_model, planner_q)
    planner.running()
