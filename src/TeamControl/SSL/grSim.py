from TeamControl.SSL.grSimUtils import grSimUtils

def run():
    ## Establish GRSIM Connection
    print(" ")
    welcome_message = f'''
    ** Welcome **
    You are now running a demo grSim Script. This will show you the basics
    Please make sure that you have double checked for your ports of connection to be:
    
    GRSIM VISION : 10020 
    GRSIM Commend sender : 20011 
    
    if not please update the ports to match both sides to establish communications.
    
    Please also make sure to enter a value for the 'ip' in grSimUtils 
    if you are trying to connect to another device's GrSim.
    
    if you have finished and checked the above, please enter 'done'
    '''      
    ans = input(welcome_message)
    if ans == "done":
        print("the grSim will now begin initialising it's connection")
    
        grSim = grSimUtils(isYellow=True)
        
        print(f"The GrSim is now connected, and is listening on {grSim.vision.port} ")
        
        print(f'''We will now enter the loop of listening to GRSIM VISION. 
              the grsim util will now deal with the listening and command sending. 
              isUpdated is a boolean that we use to determine whether we have recieved a full frame of data. 
              In particular,
              grsim : require 4 frames to be a full frame,
              real life : require 1 frame to be a full frame.
              
              Now we have a full frame, we can use it to do operations.
              The example here is make the robot move on it's x direction at a speed of 1.
              Therefore, the robot will be moving to the forward by 1 each time we recieved a full frame.
              
              Other than this operation, you can do many more other operation, such as go to target, obtacle avoidance and many more
              
              if you would like to exit at anytime, please terminate the console using :
              1. ctrl + c 
              2. close the terminal.
              
              To Continue, please presses enter.
              ''')
        ans = input()
        if ans == "":
                
            while True:
                
                isUpdated = grSim.vision.listen()
                
                if isUpdated:
                    ## DO OPERATION, e.g.
                    grSim.make_robot_move(ourTeam=True, robot_id= 0, vx = 1, vy = 0, vw = 0)
                    
                    
                
if __name__ == "__main__":
    run()