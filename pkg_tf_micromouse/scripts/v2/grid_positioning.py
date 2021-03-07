from controller_v2 import Controller
from state_v2 import State
import numpy as np 
import math

class GridPositioning(object):
    def __init__(self, size=(16, 16), dim=(2.892, 2.892)):
        self.state = State()
        self.car = Controller()
        self.current = None
        self.target = None
        self.is_aligned = False
        self.grid_location = None
        self.make_grid(size, dim)
        self.done = False
        self.ready_for_next1, self.ready_for_next2 = False, False
        self.yaw_tar_set1 = False
        self.tar_yaw = None
        self.busy = False
    def make_grid(self, size, dim):
        self.grid = np.zeros(size, dtype=tuple)
        lt_x, lt_y = (-dim[0]/2.0  + 0.02), (dim[1]/2.0 - 0.02)
        delta = 0.16 + 0.02
        print("x0, y0 ", lt_x, lt_y)
        for i in range(16): # row
            for j in range(16): # col
                self.grid[i,j] = (lt_x + j*delta + 0.08, lt_y - 0.08)
            lt_y -= delta
    
    def run(self, target_):
        self.current = [self.state.position.x, self.state.position.y, self.state.yaw ]
        # if not self.ready_for_next1 or not self.ready_for_next2: # balance in same cell
        #     c_pos = self.find_gridC(self.current)
        #     if not self.ready_for_next1 and self.move2(c_pos): self.ready_for_next1 = True 
        #     if self.check_align(): self.ready_for_next = True
        #     return False
        # else: # start moving to next cell
        #     print("######## READY FOR STEP 2 ########")
        #     return True
        self.check_sucess()
        if self.busy: return False, self.global_dir(), self.find_gridC(self.current)
        else:
            self.target = target_
            cg = self.find_gridC(self.current)
            print("G: ", cg, " T:", target_ )
            dx, dy = self.target[0] - cg[0], self.target[1] - cg[1]
            if dx > 0: self.tar_yaw = 0
            elif dx < 0: self.tar_yaw = 180
            elif dy < 0: self.tar_yaw = -90
            elif dy > 0: self.tar_yaw = 90
            else: self.tar_yaw = None
            return True, self.global_dir(), self.find_gridC(self.current)
    def reset(self):
        if self.state.position == None:
            return False, None
        self.current = [self.state.position.x, self.state.position.y, self.state.yaw ]
        return True, self.find_gridC(self.current)



    def reached(self, tar, g=1):
        if g != 1: tar = self.find_gridC(tar)
        return self.r_dist(self.grid[tar[0], tar[1]], self.current) <= 0.0001
    def find_gridC(self, cp):
        d = 10000
        pos = [-1, -1]
        for i in range(16):
            for j in range(16):
                rd = self.r_dist(self.grid[i,j], cp)
                if rd < d:
                    pos = [i, j]
                    d = rd 
        return pos
    def r_dist(self, p1, p2):
        return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ) 

    def check_align(self):
        yaw = self.current[2]
        return False

    def move2(self, tp):
        if self.reached(tp): return True
        tar, curr = self.grid[tp[0], tp[1]], self.current
        dx, dy = tar[0] - curr[0], tar[1] - curr[1]
        theta = np.arctan(dx/(dy+0.00001) ) * 180 / np.pi
        print("theta: ", theta)
        if theta >= 20 and not self.yaw_tar_set1:
            if theta >=0:
                if dy >= 0: yaw_t = -180 + theta
                else: yaw_t = theta
            else:
                if dy >=0 : yaw_t = 180 + theta
                else: yaw_t = theta
            self.yaw_tar_set1 = True
            self.tar_yaw = yaw_t
        if not self.adjust_yaw(self.tar_yaw): return False
        if not self.adjust_linear(self.r_dist(curr, tar)): return False
        return False

    def adjust_yaw(self, yaw_t):
        yaw = self.current[2]
        if yaw_t == None or abs(yaw - yaw_t) < 1: return True
        mag = yaw_t - yaw
        if abs(mag) < 20: 
            av_ = -1 * ( (mag * 3.14159 ) / 180.0 ) * 0.95
            self.car.move(lv=0, av=av_)
        else: self.car.move(lv=0, av=0.4)
        return False
    
    def adjust_linear(self, r):
        lv_ = r * 0.3
        lv_ = min(lv_ ,0.4)
        self.car.move(lv=lv_, av=0)
    
    def show_grid(self):
        for i in range(16):
            for j in range(16):
                if j==15: print("[%.3f, %.3f]"%(self.grid[i,j][0], self.grid[i,j][1]) )
                else: print("[%.3f, %.3f]"%(self.grid[i,j][0], self.grid[i,j][1]) ),
            print(" ")

    # --------------------- step 2 --------------------- #
    def check_sucess(self):
        print("CHECKING-SUCCESS")
        if self.evaluate() or self.tar_yaw == None:
            print("EVALUATING - TRUE")
            self.busy = False
            self.car.reset()
        else:
            self.busy = True
            df, av = self.check_yaw()
            if df > 1:
                self.car.move(lv = 0, av=av)
            else:
                lv = 0.25 * 20 * self.r_dist(self.current, self.grid[self.target[0], self.target[1]] ) + 0.05
                lv = min(0.4, lv)
                print("LV: ", lv, " r_D: ", self.r_dist(self.current, self.grid[self.target[0], self.target[1]] ) )
                self.car.move(lv=lv, av=0)
            print("df:", df, "av:", av)
    
    def check_yaw(self):
        print("CHECKING_YAW")
        yaw = self.current[2]
        yaw_diff, omega = 0.0, 0.0
        if self.tar_yaw == 180:
            if 180 - yaw < 1 or 180 + yaw < 1: yaw_diff = 0
            else: 
                c_wise_ = 180 + yaw
                ac_wise_ = 180- yaw
                if c_wise_ < ac_wise_: # clockwise movement
                    yaw_diff = c_wise_
                    omega = -1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
                else:                  # anti-clockwise
                    yaw_diff = ac_wise_ 
                    omega = 1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
        elif 180 - yaw < 5 or 180 + yaw < 5:
            if self.tar_yaw >= 0:
                if yaw>=0: yaw_diff = 180 - self.tar_yaw
                else: yaw_diff = 180 - self.tar_yaw + (180 + yaw)
                omega = 1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
            else:
                if yaw<0: yaw_diff = 180 + self.tar_yaw
                else: yaw_diff = 180 + self.tar_yaw + 180 - yaw
                omega = -1 * ( (yaw_diff * 3.14159 ) / 180.0 ) * 0.95
        else:
            yaw_diff = self.tar_yaw - yaw
            omega = ( (yaw_diff * 3.14159 ) / 180.0 ) * 1.2
        return abs(yaw_diff), omega
    
    def evaluate(self):
        if self.tar_yaw == None: return True
        print("yaw_t:", self.tar_yaw)
        x, y, yaw = self.current[0], self.current[1], self.current[2]
        if self.tar_yaw == 180 and not ((self.tar_yaw-yaw)<1 or (self.tar_yaw+yaw)<1): return False
        if self.tar_yaw != 180 and abs(self.tar_yaw - yaw) >= 1: return False
        tx, ty = self.grid[self.target[0], self.target[1]]
        thres = 0.01*2
        # print("TAR_YAW: ", self.tar_yaw, " T:", tx, " ", ty)
        if self.tar_yaw == 90: 
            return abs(tx+thres - x) <= 0.01
        elif self.tar_yaw == -90:
            return abs(tx-thres - x) <= 0.01
        elif self.tar_yaw == 0:
            return abs(ty-thres - y) <= 0.01
        elif self.tar_yaw == 180:
            # print("============> del_x: ", abs(ty+thres - y))
            return abs(ty+thres - y) <= 0.01
        else: return True

    def global_dir(self):
        dirs = self.availabe_dir()
        print("DIR: ", dirs)
        yaw = self.current[2]
        if abs(yaw) < 45:
            return [True, dirs[0], dirs[2], dirs[1] ]
        elif abs(yaw - 90) < 45:
            return [dirs[0], dirs[1], True, dirs[2] ]
        elif abs(yaw + 90) < 45:
            return [dirs[2], True, dirs[1], dirs[0] ]
        elif 180+yaw < 45 or 180-yaw < 45:
            return  [dirs[1], dirs[2], dirs[0], True ]
        else : return None
    def availabe_dir(self):
        lcr = [self.state.lc, self.state.fc, self.state.rc ]
        print("LCR : ", lcr)
        if lcr == None:
            return None
        else:
            if lcr[0] + lcr[2] <= 19:
                if lcr[1] < 15: return (False, False, False)
                else: return (False, True, False)
            else:
                return ( lcr[0] > 13, lcr[1] > 18, lcr[2] > 13 )

# testing ---
# ob = GridPositioning()
# ob.show_grid()
# print("-- end --")