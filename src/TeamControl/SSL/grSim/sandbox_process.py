from TeamControl.network.ssl_sockets import grSimSender
from TeamControl.network.robot_command import RobotCommand 
from TeamControl.robot.Movement import RobotMovement

def sandbox_process(wm):
    sim_ip = "127.0.0.1"
    cmd_listen_port = 20010
    is_yellow = True
    sender = grSimSender(ip=sim_ip,port=cmd_listen_port,is_yellow=is_yellow)
    
    version = 0 # vision version
    
    r = RobotMovement()
    robot_pos = 0,0,0
    ball = 0,0
    while True:
        # This is running
        # get_update
        if version < wm.get_version():
            version = wm.get_version
            try:
                robot_pos = self.wm.get_yellow_robots(isYellow=False,robot_id=self.robot_id).position
                ball = self.wm.get_latest_frame().ball.position
            except Exception :
                robot_pos = 0,0,0
                ball = 0,0
                
        vx, vy, w= RobotMovement.velocity_to_target(robot_pos=robot_pos, target=ball)
        
        cmd = RobotCommand(1, vx, vy, w, 0, 0)
        sender.send_command(cmd)