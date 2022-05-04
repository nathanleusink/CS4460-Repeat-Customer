###
# Title: vrep_controller.py
# Author: Austin Spory
###

import vrep
import sys
import time

def system_initialize():    
    global client_ID
    
    # Starting System Connection Sequence
    vrep.simxFinish(-1)
    client_ID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
    
    if(client_ID != 1):
        print("[LOG] Connected to  VREP Remote API Server")
    else:
        print("[ERROR] VREP Connection Failed")
        sys.exit("Could not connect")
    #System Connection Complete

    return client_ID


##### AUSTINS CODE GOES HERE #####
def make_sandwich():
    time.sleep(15)
