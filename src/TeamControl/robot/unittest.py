import math

import matplotlib.pyplot as plt
from TeamControl.SSL.vision.field import FieldLines, Vector2f
from TeamControl.robot.Movement import RobotMovement
from TeamControl.world.model import WorldModel

def run_test(fn):
    try:
        fn()
        print(f"[PASS] {fn.__name__}")
    except AssertionError as e:
        print(f"[FAIL] {fn.__name__}: {e}")

def test_if_ball_exist():
    robot_pos = (0.0, 0.0, 0.0)
    ball=(100.0, 0.0)

    vx, vy, w = RobotMovement.velocity_to_target(robot_pos=robot_pos, target=ball)

    assert vx != 0.0 or vy != 0.0 or w != 0.0, f"Ball does not exist printed velocities: vx={vx}, vy={vy}, w={w}"

def plot_ball_to_goal_line():
    ball = (0,0)
    goal = (1000,0)
    buffer_radius=200

    behind = RobotMovement.behind_ball_point(ball, goal, buffer_radius)
    plt.figure(figsize=(6, 6))
    plt.scatter(*ball, color='blue', label='Ball')
    plt.scatter(*goal, color='red', label='Goal')
    plt.scatter(*behind, color='green', label='Behind Ball (Robot Target)')

    # Plot lines
    plt.plot([ball[0], goal[0]], [ball[1], goal[1]], 'r--', label='Ball → Goal')
    plt.plot([ball[0], behind[0]], [ball[1], behind[1]], 'g--', label='Ball → Behind')
    
    # Decorations
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Behind-Ball Geometry Check")
    
    plt.show()

def plot_ball_to_goal():
    

    # ---- dimensions (mm) ----
    
    length= 4500
    width = 3000     # half field size
    margin = 300                     # field margin
    line_thickness = 1              # line thickness
    penalty_length = 2000
    penalty_width = 1000
    center_circle = 500

    outer_length = length + margin
    outer_width = width + margin

    def line(x1, y1, x2, y2):
        return FieldLines("", Vector2f(x1, y1), Vector2f(x2, y2), line_thickness)

    # ---- field lines ----
    field = [
        # main field
        line(-length,  width,  length,  width), # top line
        line(-length, -width,  length, -width), # bottom line
        line(-length, -width, -length,  width), # left line
        line( length, -width,  length,  width), # right line   
        line(0, -width, 0, width),
        line(-length,  0, length, 0),

        # left penalty box
        line(-length,  penalty_width, -length + penalty_width,  penalty_width),
        line(-length, -penalty_width, -length + penalty_width, -penalty_width),
        line(-length + penalty_width, -penalty_width, -length + penalty_width,  penalty_width),

        # right penalty box
        line(length,  penalty_width, length - penalty_width,  penalty_width),   # top
        line(length, -penalty_width, length - penalty_width, -penalty_width),   # bottom
        line(length - penalty_width, -penalty_width, length - penalty_width,  penalty_width),

        # left goal
        line(-length-200,1000/2,-length,1000/2),
        line(-length-200,-1000/2,-length,-1000/2),
        line(-length-200,1000/2,-length-200,-1000/2),

        line(length,  1000/2, length + 200,  1000/2),   # top
        line(length, -1000/2, length + 200, -1000/2),   # bottom
        line(length + 200, 1000/2, length + 200, -1000/2)  # back vertical
    ]

    # ---- draw 
    fig, ax = plt.subplots(figsize=(10, 7))

    # green background (field + margin)
    ax.add_patch(
        plt.Rectangle(
            (-outer_length, -outer_width),
            2 * outer_length,
            2 * outer_width,
            color="green",
            zorder=0
        )
    )

    for l in field:
        ax.plot([l.p1.x, l.p2.x], [l.p1.y, l.p2.y],
                linewidth=l.thickness, color="white")

    # center circle
    ax.add_patch(plt.Circle((0, 0), center_circle, fill=False,
                            linewidth=line_thickness, color="white"))

    ax.set_aspect("equal") # keep the field ratio correct
    ax.axis("off")

    # draw ball to goal line

    # wm = WorldModel(update_interval=10, history=60, use_sim=True)
    # frame = wm.get_latest_frame()
    # ball_pos = (frame.ball.x, frame.ball.y)
    # robot_pos = (frame.robots_yellow[0].x, frame.robots_yellow[0].y)

    ball_pos = (4000, 0)          # Ball at center
    goal_pos = (450, 103)       # Right goal
    buffer_radius = 200
    
    
    behind_pos = RobotMovement.behind_ball_point(ball_pos, goal_pos, buffer_radius)

    # Plot ball and goal
    plt.scatter(*ball_pos, color='blue', label='Ball')
    plt.scatter(*goal_pos, color='red', label='Goal')

    # Plot the line
    plt.plot([ball_pos[0], goal_pos[0]], [ball_pos[1], goal_pos[1]], 'r--', label='Ball → Goal')

   # Decorations
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.grid(True)
    plt.axis('equal')
    
    plt.show()


run_test(plot_ball_to_goal)


