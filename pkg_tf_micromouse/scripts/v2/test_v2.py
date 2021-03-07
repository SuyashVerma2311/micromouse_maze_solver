from path_planner import Planner
from state_v2 import State
from controller_v2 import Controller
from grid_positioning import GridPositioning
from explorer import Explorer
import numpy as np
import rospy
import cv2
import random
import time
start_time = time.time()

def sample(d):
    x = []
    for i in range(len(d)):
        if d[i]: x.append(i)
    randi = random.randint(0,len(x)-1)
    return x[randi]
soln = [ [0,0], [1,0], [1,1], [2,1], [3,1], [3,2], [3,3], [4,3], [5,3], [5,2], [6,2], [7,2],
        [8,2], [8,3], [8,4], [7,4], [6,4], [6,5], [5,5], [5,6], [6,6], [7,6], [7,7] ]
soln_prats = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [6, 0], [5, 0], [4, 0], [3, 0], [2, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 2], [4, 2], [3, 2], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [6, 3], [5, 3], [5, 4], [5, 3], [4, 3], [4, 4], [3, 4], [3, 5], [4, 5], [3, 5], [3, 4], [4, 4], [4, 3], [5, 3], [5, 2], [6, 2], [7, 2], [8, 2], [8, 3], [8, 4], [8, 5], [8, 4], [7, 4], [6, 4], [6, 5], [5, 5], [5, 6], [6, 6], [7, 6], [7, 7]]
soln = soln_prats
pre = 0

rospy.init_node("testing_version_2")
cv2.namedWindow("Testing_v2", 100)

# pp = Planner()
gp = GridPositioning()
# state = pp.state
dora = Explorer([1,0])
state = gp.state
tar , sam = soln[0], 0
# tar , sam = [1,0], 0
tar_ar = []
f = False
while not rospy.is_shutdown():
    # gp.state.display()
    # print(" -- -- -- -- ")
    k = cv2.waitKey(30)
    if k == 27: break
    k = k - 48
    if gp.current != None: print(" c: ", gp.find_gridC(gp.current))
    if f : k = 0
    if k == 0:
        f = True
        """
        if tar == None: tar = [pp.state.position.x, pp.state.position.y]
        done = pp.run(tar)
        print("done: ", done)
        if done: 
            tar = [tar[0]+0.17, tar[1]+0.02 ]
            if tf == 2: break
            tf += 1
            print("############ TARGET RESET ############")
        """
        # gp.state.display()
        print(" -- -- -- -- ")
        res, nxt, cur = gp.run(tar)
        print("TAR: ", tar, " CUR: ", cur)
        print("NXT: ", nxt)
        if res:
            print("NEXT:(NEWS) ", nxt, "CUR: ", cur)
            # mv = sample(nxt)
            if soln[pre] == cur and tar == cur:
                pre += 1
                if pre == len(soln): break
                tar = soln[pre]
            # if tar == cur:
            #     tar = dora.run(cur, nxt)
            #     tar_ar.append([cur,tar,nxt])

            """
            if cur[0] != tar[0] and cur[1] != tar[1]:
                continue 
            mv = int(input("NEXT MOVE: "))
            if mv == 6 : tar = [cur[0], cur[1]+1]
            elif mv == 8 : tar = [cur[0]-1, cur[1]]
            elif mv == 4 : tar = [cur[0], cur[1]-1]
            else: tar = [cur[0]+1, cur[1]]
            """
            sam += 1
            # tar_ar.append([cur,tar,nxt])
    else:
        # pp.car.key_run(k)
        gp.car.key_run(k)
    print(" -- -- -- -- ", k, " sam: ", sam )

print("t: ", tar_ar)
print("## end ##")
print("TIME: ", (time.time() - start_time)/60.0 )
# dora.show_map()
