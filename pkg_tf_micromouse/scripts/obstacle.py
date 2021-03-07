import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import numpy as np

class Obstacle(object):
    def __init__(self, delta_err=3):
        self.sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, self.clbk_laser)
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.clbk_odom)
        self.dist2wall = None
        self.lcr = None # left-center-right
        self.position = None
        self.yaw = None

    def clbk_laser(self, msg):
        # print("size: ", len(msg.ranges))
        self.dist2wall = [
            round(100*min(min(msg.ranges[0:71]), 100)),
            round(100*min(min(msg.ranges[72:143]), 100)),
            round(100*min(min(msg.ranges[144:215]), 100)),
            round(100*min(min(msg.ranges[216:287]), 100)),
            round(100*min(min(msg.ranges[288:359]), 100)),
        ]
        self.lcr = [self.dist2wall[4], self.dist2wall[2], self.dist2wall[0]]

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

    def get_state(self):
        return {"pos": self.position, "yaw": self.yaw }

    def display(self):
        print("d2w: ", self.dist2wall)
        print("lcr: ", self.lcr)
        print("pos: ", self.position)
        print("yaw: ", self.yaw)