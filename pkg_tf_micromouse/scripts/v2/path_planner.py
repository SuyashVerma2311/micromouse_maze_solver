from controller_v2 import Controller
from state_v2 import State
import numpy as np 
import math

class Planner(object):
    def __init__(self, delta_er = 0.1):
        self.state = State()
        self.car = Controller()
        self.target = None
        self.local_tar = None
        self.tar_yaw = None
        self.current = None
        self.done = True
        self.is_aligned = True
        self.collision = False
        self.done_yaw = False

    def run(self, target_):
        self.target = target_
        if self.update(): 
            self.car.reset()
            return True
        print("r_d: ", self.r_dist(self.current, self.target)) 
        print("c: %.4f, %.4f, t: %.4f, %.4f"%(self.current[0], self.current[1], self.target[0], self.target[1]) )
        return self.go2target()

    def update(self):
        self.current = [self.state.position.x, self.state.position.y, self.state.yaw]
        if self.target == None: self.target = [self.current[0], self.current[1] ]
        return self.r_dist(self.current, self.target) <= 0.0001
    def r_dist(self, p1, p2):
        return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ) 

    def go2target(self): 
        if not self.collision:
            if not self.adjust_yaw(): return False
        # print("####### adjust-yaw done #######")
        if not self.adjust_linear(): return False
        return True
    
    # --------------------- yaw adjustment ----------------------- # 
    def adjust_yaw(self):
        x, y, yaw = self.current[0], self.current[1], self.current[2]
        xt, yt = self.target[0], self.target[1]
        dx, dy = xt - x, yt - y
        theta = np.arctan(dx/dy) * 180 / np.pi
        yaw_t = 0.0
        if abs(theta) <= 45 and dy > 0: # target-yaw is 0
            yaw_t = 0
        elif abs(theta) <= 45 and dy < 0: # target-yaw is 180
            yaw_t = 180
        elif abs(90 - theta) <= 45: # target-yaw is 90
            yaw_t = 90
        else: yaw_t = -90
        self.tar_yaw = yaw_t
        df, om = self.check_yaw(yaw_t, yaw)
        print("diff yaw: yt - y ", yaw_t, " ",  yaw," | df:", df, " om:", om )
        if df < 1: return True
        self.car.move(lv = 0, av = om)
        return False

    def check_yaw(self, yaw_t, yaw):
        self.yaw = yaw
        yaw_diff, omega = 0.0, 0.0
        if yaw_t == 180:
            if 180 - self.yaw < 1 or 180 + self.yaw < 1: yaw_diff = 0
            else: 
                c_wise_ = 180 + self.yaw
                ac_wise_ = 180- self.yaw
                if c_wise_ < ac_wise_: # clockwise movement
                    yaw_diff = c_wise_
                    omega = -1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
                else:                  # anti-clockwise
                    yaw_diff = ac_wise_ 
                    omega = 1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
        elif 180 - self.yaw < 1 or 180 + self.yaw < 1:
            if yaw_t >= 0:
                yaw_diff = 180 - self.yaw
                omega = -1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
            else:
                yaw_diff = 180 + self.yaw
                omega = 1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
        else:
            yaw_diff = yaw_t - self.yaw
            omega = ( (yaw_diff * 3.14159 ) / 180.0 ) * 1.2
        return abs(yaw_diff), omega

    # ----------------------- linear velocity -------------------- #
    def adjust_linear(self):
        # propertional speed
        # maintain side-gap from wall 8.5 cm/wall
        # check for collision - progress...
        # reset_target
        self.check_positioning()
        if self.check_collision(): return False
        r = self.r_dist(self.current, self.target)
        lv = min(r*3, 0.4)
        if r > 0.0001: self.car.move(lv = lv, av=0) 
        else: return True
        return False
    def check_collision(self):
        r, fr, f, fl, l = self.state.dist2wall
        lc, fc, rc = self.state.lc, self.state.fc, self.state.rc
        if fr > 10 and f > 10 and fl > 10:
            self.collision = False
            return False
        if fr < 10 and (f > 12 or fl > 12):
            self.car.move(lv=0.2, av=0.78)
        elif fl < 10 and (f > 12 or fr > 12):
            self.car.move(lv=0.2, av=-0.78)
        elif f < 10 and ( fl > 12 or fr > 12):
            if fl > 12: self.car.move(lv=0.2, av=-0.78)
            else: self.car.move(lv=0.2, av=0.78)
        else:
            print(" ELSE PART")
            # self.car.reset()
            self.collision = False
            return False
        print("************ COLLISION ************")
        self.collision = True
        return True
        
    def check_positioning(self):
        lc, fc, rc = self.state.lc, self.state.fc, self.state.rc
        fnbox, frem = fc/18, fc%18
        lnbox, lrem = lc/18, lc%18
        rnbox, rrem = rc/18, rc%18
        dx, dy = self.target[0] - self.current[0], self.target[1] - self.current[1]
        ex = 1  


        
        


        
        
        


    

