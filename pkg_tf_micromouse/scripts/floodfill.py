#! /usr/bin/env python
import numpy as np

class FloodFill(object):
    def __init__(self):
        ### ALERT : self.pos (or) pos should be integer tuple of 2 elements ###
        #self.pos = pos                                                                   # This will keep track of current location #
        self.val = 255                                                                   # This will hold the flood val of the current cell #
        self.path=[[0,0]] #for sample maze 2
        self.path_return=[]
        self.mode = "discovery"                                                          # This is meant to use different forms of the class #
        self.stack = []
        self.flag=0
        ### Initial Cell Map Floodfill ###                                               # This will keep track of current flooding on the map #
        self.cell_map= np.array([[14,13,12,11,10, 9, 8, 7, 7, 8, 9,10,11,12,13,14],
                                 [13,12,11,10, 9, 8, 7, 6, 6, 7, 8, 9,10,11,12,13],
                                 [12,11,10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9,10,11,12],
                                 [11,10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9,10,11],
                                 [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9,10],
                                 [ 9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
                                 [ 8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
                                 [ 7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
                                 [ 7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
                                 [ 8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
                                 [ 9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
                                 [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9,10],
                                 [11,10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9,10,11],
                                 [12,11,10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9,10,11,12],
                                 [13,12,11,10, 9, 8, 7, 6, 6, 7, 8, 9,10,11,12,13],
                                 [14,13,12,11,10, 9, 8, 7, 7, 8, 9,10,11,12,13,14]])
        ### Initial Wall Map ###                                                         # This will keep track of all the walls that are discovered #
        ### Initially Walls only on the edges of the arena ###
        self.wall_map_v= np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  #vertical wall map
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
        self.wall_map_h=np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],    #horizontal wall map
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
        """
        self.wall_map_v= np.array([[1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],  #vertical wall map
                                 [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                                 [1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
                                 [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
                                 [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1],
                                 [1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
                                 [1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
                                 [1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1],
                                 [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                                 [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                                 [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                                 [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
                                 [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
                                 [1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]])
        self.wall_map_h=np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],    #horizontal wall map
                                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
                                  [0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                                  [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
                                  [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0],
                                  [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                  [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                                  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                                  [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                                  [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
                                  [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
                                  [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                                  [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0],
                                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
        """
        #print(self.wall_map_h)
        l=[[0 for i in range(16)]for i in range(16)]
        for i in range(16):
            ctr=i
            for j in range(16):
                l[i][j]=ctr
                ctr=ctr+1
        self.cell_map_return=np.array(l)
        print(self.cell_map_return)        

    def update(self, pos, walls=[0,0,0,0]):
        # Updating the position, holding the value and clearing the stack #
        if pos == (7, 7) or pos == (7, 8) or pos == (8, 7) or pos == (8, 8) :
            self.flag=1
            return self.update_return(pos, walls)
        if self.flag==1:
            return self.update_return(pos, walls)   
        self.pos = pos
        self.val = self.cell_map[self.pos[0]][self.pos[1]]
        self.stack = []
        self.flag=0
        # Updating the Wall Map #
        walls = np.array(walls, dtype=bool)
        if walls[0]: ### North Update ###
            self.wall_map_h[self.pos[0]][self.pos[1]] = 1
        if walls[1]: ### East Update ###
            self.wall_map_v[self.pos[0]][self.pos[1]+1] = 1
        if walls[2]: ### West Update ###
            self.wall_map_v[self.pos[0]][self.pos[1]] = 1
        if walls[3]: ### South Update ###
            self.wall_map_h[self.pos[0]+1][self.pos[1]] = 1

        # Main Loop for updating the values of the cells in stack #
        # This loop will update the flood values for the cells #
        self.stack.append(pos)
        open_neighbors_val = []
        open_neighbors = []
        my_neighbors = []
        my_neighbors_val = []

        if not self.wall_map_h[pos[0]+1][pos[1]]:  #south check
            my_neighbors.append([pos[0]+1, pos[1]])
        if not self.wall_map_h[pos[0]][pos[1]]: #north check
            my_neighbors.append([pos[0]-1, pos[1]])
        if not self.wall_map_v[pos[0]][pos[1]+1]: #east check
            my_neighbors.append([pos[0], pos[1]+1])
        if not self.wall_map_v[pos[0]][pos[1]]:  #west check
            my_neighbors.append([pos[0], pos[1]-1])    
        if len(open_neighbors)==1:
            print("blocked at ",pos)                

        while len(self.stack) != 0:
            popped_cell = self.stack.pop()
            popped_val = self.cell_map[popped_cell[0]][popped_cell[1]]
            # open_neighbors.clear()
            del open_neighbors[:]
            # open_neighbors_val.clear()
            del open_neighbors_val[:]

            if not self.wall_map_h[popped_cell[0]+1][popped_cell[1]]:  #south check
                open_neighbors.append([popped_cell[0]+1, popped_cell[1]])
            if not self.wall_map_h[popped_cell[0]][popped_cell[1]]: #north check
                open_neighbors.append([popped_cell[0]-1, popped_cell[1]])
            if not self.wall_map_v[popped_cell[0]][popped_cell[1]+1]: #east check
                open_neighbors.append([popped_cell[0], popped_cell[1]+1])
            if not self.wall_map_v[popped_cell[0]][popped_cell[1]]:  #west check
                open_neighbors.append([popped_cell[0], popped_cell[1]-1])

            # if len(open_neighbors)==1:
            #     print("blocked at ",)
            for neighbor in open_neighbors:
                open_neighbors_val.append(self.cell_map[neighbor[0]][neighbor[1]])

            #print("open neighbors for ",popped_cell," ",open_neighbors)
            if popped_val != 1 + min(open_neighbors_val):
                self.cell_map[popped_cell[0]][popped_cell[1]] = 1 + min(open_neighbors_val)
                #print("cell value changed")
                for neighbor in open_neighbors:
                    self.stack.append(neighbor)
        for neighbor in my_neighbors:
            my_neighbors_val.append(self.cell_map[neighbor[0]][neighbor[1]])
        next_pos = my_neighbors[my_neighbors_val.index(min(my_neighbors_val))]    
        # my_neighbors.clear()
        del my_neighbors[:]
        # my_neighbors_val.clear()
        del my_neighbors_val[:]
        self.path.append(next_pos)
        return next_pos
        # if next_pos==[7,7] or next_pos==[7,8] or next_pos==[8,7]:
        #     print("next step is destination")
        #     return next_pos
        # else:
        #     print("going to ",next_pos)
        #      return self.update(tuple(next_pos),[0,0,0,0])      

    def update_return(self, pos, walls=[0,0,0,0]):
        # Updating the position, holding the value and clearing the stack #
        print("RETURING HOME")
        if pos == (0, 0) :
            self.flag=0
            return self.update(pos, walls)
        self.pos = pos
        self.val = self.cell_map_return[self.pos[0]][self.pos[1]]
        self.stack = []

        # Updating the Wall Map #
        walls = np.array(walls, dtype=bool)
        if walls[0]: ### North Update ###
            self.wall_map_h[self.pos[0]][self.pos[1]] = 1
        if walls[1]: ### East Update ###
            self.wall_map_v[self.pos[0]][self.pos[1]+1] = 1
        if walls[2]: ### West Update ###
            self.wall_map_v[self.pos[0]][self.pos[1]] = 1
        if walls[3]: ### South Update ###
            self.wall_map_h[self.pos[0]+1][self.pos[1]] = 1

        # Main Loop for updating the values of the cells in stack #
        # This loop will update the flood values for the cells #
        self.stack.append(pos)
        open_neighbors_val = []
        open_neighbors = []
        my_neighbors = []
        my_neighbors_val = []

        if not self.wall_map_h[pos[0]+1][pos[1]]:  #south check
            my_neighbors.append([pos[0]+1, pos[1]])
        if not self.wall_map_h[pos[0]][pos[1]]: #north check
            my_neighbors.append([pos[0]-1, pos[1]])
        if not self.wall_map_v[pos[0]][pos[1]+1]: #east check
            my_neighbors.append([pos[0], pos[1]+1])
        if not self.wall_map_v[pos[0]][pos[1]]:  #west check
            my_neighbors.append([pos[0], pos[1]-1])    
        if len(open_neighbors)==1:
            print("blocked at ",pos)                

        while len(self.stack) != 0:
            popped_cell = self.stack.pop()
            popped_val = self.cell_map_return[popped_cell[0]][popped_cell[1]]
            # open_neighbors.clear()
            del open_neighbors[:]
            # open_neighbors_val.clear()
            del open_neighbors_val[:]

            if not self.wall_map_h[popped_cell[0]+1][popped_cell[1]]:  #south check
                open_neighbors.append([popped_cell[0]+1, popped_cell[1]])
            if not self.wall_map_h[popped_cell[0]][popped_cell[1]]: #north check
                open_neighbors.append([popped_cell[0]-1, popped_cell[1]])
            if not self.wall_map_v[popped_cell[0]][popped_cell[1]+1]: #east check
                open_neighbors.append([popped_cell[0], popped_cell[1]+1])
            if not self.wall_map_v[popped_cell[0]][popped_cell[1]]:  #west check
                open_neighbors.append([popped_cell[0], popped_cell[1]-1])

            # if len(open_neighbors)==1:
            #     print("blocked at ",)
            for neighbor in open_neighbors:
                open_neighbors_val.append(self.cell_map_return[neighbor[0]][neighbor[1]])

            #print("open neighbors for ",popped_cell," ",open_neighbors)
            if popped_val != 1 + min(open_neighbors_val):
                self.cell_map_return[popped_cell[0]][popped_cell[1]] = 1 + min(open_neighbors_val)
                #print("cell value changed")
                for neighbor in open_neighbors:
                    self.stack.append(neighbor)
        for neighbor in my_neighbors:
            my_neighbors_val.append(self.cell_map_return[neighbor[0]][neighbor[1]])
        next_pos = my_neighbors[my_neighbors_val.index(min(my_neighbors_val))]    
        # my_neighbors.clear()
        del my_neighbors[:]
        # my_neighbors_val.clear()
        del my_neighbors_val[:]
        self.path_return.append(next_pos)
        return next_pos
        # if next_pos==[0,0]:
        #     print("next step is starting point")
        #     #self.path_return.append(next_pos)
        #     return next_pos
        # else:
        #     print("going to ",next_pos)
        #     return self.update_return(tuple(next_pos),[0,0,0,0])            


# ff=FloodFill()


# #print(ff.update((2,1),[0,1,0,0]))
# #print(ff.update((3,1),[0,1,0,0]))
# #print(ff.update((4,1),[0,1,0,0]))
# #print(ff.update((5,1),[0,1,1,1]))
# #print(ff.update((0,0),[0,1,1,0]))
# #print(ff.update((1,0),[0,0,1,0]))
# #print(ff.update((2,0),[0,1,1,1]))

# #----------test for sample maze 2--------
# # if ff.update((0,0),[0,0,0,0])==[1,0]:
# #     print("testing")
# ff.update_return(ff.update((0,0),[0,0,0,0]))
# #print(ff.update((0,0),[0,0,0,0])[:,-1])
# print(ff.cell_map)
# print(ff.path,"initial steps ",len(ff.path))
# print("return path \n",ff.path_return, " steps ",len(ff.path_return))
# ff.path.clear()
# print(ff.path)
# ff.path_return.clear()
# ff.update_return(ff.update((0,0),[0,0,0,0]))
# #ff.update((0,0),[0,0,0,0])
# print("final path \n", ff.path,"final steps ",len(ff.path))
# print("return path \n",ff.path_return, " steps ",len(ff.path_return))
# ff.path.clear()
# ff.path_return.clear()
# #ff.update((0,0),[0,0,0,0])
# ff.update_return(ff.update((0,0),[0,0,0,0]))
# print("final path 2 \n", ff.path,"final steps 2 ",len(ff.path))
# print("return path \n",ff.path_return, " steps ",len(ff.path_return))
# ff.path.clear()
# ff.path_return.clear()
# #ff.update((0,0),[0,0,0,0])
# ff.update_return(ff.update((0,0),[0,0,0,0]))
# print("final path 3 \n", ff.path,"final steps 3 ",len(ff.path))
# print("return path \n",ff.path_return, " steps ",len(ff.path_return))
# print(ff.cell_map)
# print(ff.cell_map_return)
# #print(ff.wall_map_v)
# #print(ff.wall_map_h)        
