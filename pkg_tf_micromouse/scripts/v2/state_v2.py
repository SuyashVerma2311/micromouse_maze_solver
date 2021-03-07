import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import numpy as np
import matplotlib.pyplot as plt 

class State(object):
    def __init__(self):
        self.sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, self.clbk_laser)
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.clbk_odom)
        self.dist2wall = None
        self.fc = None
        self.lc = None
        self.rc = None
        self.lcr = None # left-center-right
        self.position = None
        self.yaw = None
        self.lidar_data = None
    
    def clbk_laser(self, msg):
        # print("size: ", len(msg.ranges))
        self.lidar_data = msg.ranges
        self.dist2wall = [
            round(100*min(min(msg.ranges[0:71]), 100)),
            round(100*min(min(msg.ranges[72:143]), 100)),
            round(100*min(min(msg.ranges[144:215]), 100)),
            round(100*min(min(msg.ranges[216:287]), 100)),
            round(100*min(min(msg.ranges[288:359]), 100)),
        ]
        self.lcr = [self.dist2wall[4], self.dist2wall[2], self.dist2wall[0]]
        self.fc =  round(100*min(min(msg.ranges[177:183]), 100))
        self.lc = round(100*min(min(msg.ranges[354:359]), 100))
        self.rc = round(100*min(min(msg.ranges[0:6]), 100))

    def clbk_odom(self, msg):
        # position
        self.position = msg.pose.pose.position
        # yaw
        quaternion = (
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w)
        euler = transformations.euler_from_quaternion(quaternion)
        self.yaw = (euler[2]* 180.0) / np.pi
        # 0=S, 90=E, 180/-180=N, -90=W
    
    def get_state(self):
        return {"pos": self.position, "yaw": self.yaw, "clearance" : [self.lc, self.fc, self.rc] }

    def display(self):
        print("d2w: ", self.dist2wall)
        print("lcr: ", self.lcr)
        print("pos: ", self.position)
        print("yaw: ", self.yaw)
    
    def plot(self, str_):
        if str_ == "right": plt.plot(self.lidar_data[0:72])
        elif str_ == "front-right": plt.plot(self.lidar_data[72:144])
        elif str_ == "front-left": plt.plot(self.lidar_data[216:288])
        elif str_ == "left": plt.plot(self.lidar_data[288:360])
        else: plt.plot(self.lidar_data[144:216])
        plt.draw()
        plt.pause(1e-6)
        plt.clf()
