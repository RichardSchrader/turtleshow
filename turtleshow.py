###############################################################################
# Filename: turtleshow.py
# Author: Richard Schrader
# Date: 14MAR21
###############################################################################
# Contributors:
#
###############################################################################
# Note:
#   Using turtles as drones to draw some figure patterns like a drone show.
###############################################################################
# Revision history:
# - 14MAR21 - turtle fleet created and doing the minimal path to reach the
#             pattern point.
#
# TODO - calculate the optimal solution for minimal path if necessary avoiding
#        collison. (calculate the min path from all turtles to all target points and minimizing the sum)
#      - implement some cool way to load the target pattern points.
#      - ... etc...


from turtle import *
import numpy as np
import math

class Drone(Turtle):

    def __init__(self):
        '''Global inicialization for all Drone objects.'''
        super().__init__()
        self.shape('turtle')    # Turtle shape form.
        self.up()               # No drawing when moving.
        self.speed(2)           # Movement speed.
        self.setpos(-400,-400)

    def getpos(self):
        return self.pos()

    def gopos(self, pos):
        self.setpos(pos)

class DroneFleet:

    def __init__(self, size):
        self.size = size
        self.fleet = [Drone() for i in range(size)]

    def init(self):
        for i, drone in enumerate(self.fleet):
            drone.forward(20 * i)

    def getpos(self):
        pos_array = []
        [pos_array.append(self.fleet[i].getpos()) for i in range(self.size)]
        return np.array(pos_array)

    def gopos(self, pos_array):
        [self.fleet[i].gopos(pos) for i, pos in enumerate(pos_array.tolist())]

    def gominpos(self, dist_min_index_array, target):
        for i in reversed(range(len(dist_min_index_array))):
            self.fleet[dist_min_index_array[i][0]].gopos(target[dist_min_index_array[i][1]])

        #[self.fleet[index[0]].gopos(index[1]) for index in dist_min_index_array]


def dist_array(pos, target_array):
    dist_array = []
    [dist_array.append(math.dist(pos, target)) for target in target_array.tolist()]
    return dist_array

def dist_matrix(pos_array, target_array):
    dist_matrix = []
    [dist_matrix.append(dist_array(pos, target_array)) for pos in pos_array.tolist()]
    return np.array(dist_matrix)

def dist_min_index_array(fleet, target_array):
    a = dist_matrix(fleet.getpos(), target_array)
    go_array = []
    for i in range(a.shape[0]):
        ind = np.unravel_index(np.argmin(a, axis=None), a.shape)
        go_array.append(ind)
        a[ind[0], :] = np.inf
        a[:, ind[1]] = np.inf  
    return go_array


wn = Screen()

f1=DroneFleet(49) 
f1.init()
print(f1.getpos()) 
target = np.array([[0, 100], [50, 50], [-50, 50], [-50, -50], [50, -50], [0, -100], [-100, 0], [100, 0], [100, 100],
[-100, 100], [100, -100], [-100, -100], [0, 0], [0, 150], [0, -150], [150, 0], [-150, 0], [150, -150], [-150, 150],
[-150, -150], [150, 150], [150, 100], [-150, 100], [150, -100], [-150, -100], [100, 150], [-100, 150], [100, -150],
[-100, -150], [100, 50], [-100, 50], [100, -50], [-100, -50], [50, 100], [-50, 100], [50, -100], [-50, -100], [50, 0],
[0, 50], [-50, 0], [0, -50], [150, 50], [-150, 50], [150, -50], [-150, -50], [50, 150], [50, -150], [-50, 150], [-50, -150]])
print(target)
out = dist_min_index_array(f1, target)
print(out)
f1.gominpos(out, target)

wn.exitonclick()
