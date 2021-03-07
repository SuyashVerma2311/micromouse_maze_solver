import numpy as np
import random
import time

class Node(object):
    def __init__(self, d=100000):
        self.dist2home = d
        self.is_dead = False
        self.N = None
        self.E = None
        self.W = None
        self.S = None
        self.dirs = None
        self.is_explored = False
    def assign_dir(self, dirs):
        self.dirs = dirs
        self.N, self.E, self.W, self.S =  dirs
    def mark_dead(self):
        self.is_dead = True
    def explored(self):
        self.is_explored = True

class Explorer(Node):
    def __init__(self, start, dim=(16, 16)):
        self.map = []
        self.start_time = time.time()
        self.last_pos = None
        self.start = start
        self.curr_pos = None
        self.nodes_explored = 0
        self.construct_map(dim)
        self.mode = "explore"
        self.weight = [0, 0, 0, 0]
    def construct_map(self, dim):
        row, col = dim
        for i in range(row):
            temp = []
            for j in range(col):
                temp.append(Node())
            self.map.append(temp)
    
    def run(self, cur, free_dir):
        self.curr_pos = cur
        x, y = cur
        if not self.map[x][y].is_explored:
            self.add2map(cur, free_dir)
        return self.decide()

    def add2map(self, cur, fdir):
        print("ADDING TO MAP")
        x, y = cur
        self.nodes_explored += 1
        self.map[x][y].explored()
        self.map[x][y].assign_dir(fdir)
        if self.last_pos == None:
            self.map[x][y].dist2home = 0
        else:
            m = 10000
            if x > 0 and self.map[x-1][y].dist2home < m: m = self.map[x-1][y].dist2home
            if x < len(self.map)-1 and self.map[x+1][y].dist2home < m: m = self.map[x+1][y].dist2home 
            if y > 0 and self.map[x][y-1].dist2home < m: m = self.map[x][y-1].dist2home
            if y < len(self.map[0])-1 and self.map[x][y+1].dist2home < m: m = self.map[x][y+1].dist2home
            self.map[x][y].dist2home = m + 1

    def decide(self):
        x, y = self.curr_pos
        if self.is_dead_end():
            self.map[x][y].mark_dead()
        self.last_pos = [x, y]
        return self.next_move()

    def is_dead_end(self):
        x, y = self.curr_pos
        n, e, w, s =  self.map[x][y].dirs 
        fr = 0
        self.weight = [0, 0, 0, 0]
        if n and not self.map[x-1][y].is_dead: 
            fr += 1
            self.weight[0] = 1
        if s and not self.map[x+1][y].is_dead: 
            fr += 1
            self.weight[3] = 1
        if e and not self.map[x][y+1].is_dead:
            fr += 1
            self.weight[1] = 1
        if w and not self.map[x][y-1].is_dead: 
            fr += 1
            self.weight[2] = 1
        if fr <= 1: return True
        return False

    def next_move(self):
        x, y = self.curr_pos
        # n, e, w, s =  self.map[x][y].dirs
        print("NEXT MOVE : ", self.weight)
        if self.weight[0] and not self.map[x-1][y].is_explored: self.weight[0] += 1
        if self.weight[1] and not self.map[x][y+1].is_explored: self.weight[1] += 1
        if self.weight[2] and not self.map[x][y-1].is_explored: self.weight[2] += 1
        if self.weight[3] and not self.map[x+1][y].is_explored: self.weight[3] += 1
        m, p = 0, -1
        for j in range(4):
            if self.weight[j] > m:
                m = self.weight[j]
                p = j
        print("F-w: ", self.weight, " p:", p)
        if p == 0: return [x-1, y]
        if p == 1: return [x, y+1]
        if p == 2: return [x, y-1]
        if p == 3: return [x+1, y]
        return [x, y]
    
    def show_map(self):
        row = len(self.map)
        for i in range(row):
            print("["),
            for ob in self.map[i]:
                if ob.dist2home == 100000: print("---"),
                elif ob.dist2home < 10: print("00"+str(ob.dist2home)),
                elif ob.dist2home < 100: print("0"+str(ob.dist2home)),
                else: print(ob.dist2home),
            print("]")
        for i in range(row):
            print("["),
            for ob in self.map[i]:
                if ob.is_explored and ob.is_dead: print("2"),
                elif ob.is_explored: print("1"),
                else: print("0"),
            print("]")
        print("TIME: ", (time.time()-self.start_time)/60.0 )

# testing -- 
# dora = Explorer(start=[0,0])
# dora.show_map()
# print(dora.map[1][2])

