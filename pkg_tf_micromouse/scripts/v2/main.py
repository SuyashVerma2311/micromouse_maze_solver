from path_planner import Planner
from state_v2 import State
from controller_v2 import Controller
from grid_positioning import GridPositioning
from explorer import Explorer
from floodfill import FloodFill
import numpy as np
import rospy
import cv2
import time
start_time = time.time()

rospy.init_node("testing_version_2")
cv2.namedWindow("Control-Window", 100)

gp = GridPositioning()
res, cur = False, None
while not res:
    res, cur = gp.reset()
k, last_k = 1, 0
target_logs = []

# dora = Explorer(cur) # replace with flood-fill
dora = FloodFill()

while not rospy.is_shutdown():
    key = cv2.waitKey(30)
    if key == 27: break
    else: 
        key = key - 48
        if key == 0: k = 0
        if key == 1: k = 1
    
    if k == 1:
        print("MANUAL-MODE")
        gp.car.key_run(key)

    if k == 0:
        print("AUTONOMOUS-MODE")
        if last_k != 0:
            r, cur = gp.reset() 
            tar = cur
            print("---> RESET: ", cur, " ", tar)
        res, fdir, cur = gp.run(tar)
        print("C: ", cur, " T:", tar)
        if res and tar == cur:
            # tar = dora.run(cur, fdir)
            tar = dora.update((cur[0], cur[1]), [not i for i in fdir])
            target_logs.append([cur, tar, fdir])
            print("RESET: ", cur, " ", tar)
    last_k = k
print("<- END ->")
print(target_logs)
print( "TIME: ", (time.time() - start_time)/60.0 )
print(dora.cell_map)
    




