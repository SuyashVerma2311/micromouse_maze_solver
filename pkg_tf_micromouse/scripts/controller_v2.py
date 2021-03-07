import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import numpy as np

class Controller(object):
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.vel = None
        self.ang_vel = None
        self.msg_pub = Twist()
    def move(self, lv=0.3, av=0):
        self.vel = lv
        self.ang_vel = av
        self.msg_pub.linear.x = self.vel
        self.msg_pub.angular.z = self.ang_vel
        self.execute()
    def reset(self):
        self.msg_pub = Twist()
        self.move(lv=0, av=0)
    def turn_left(self, ang = 0.3):
        self.msg_pub.angular.z = ang
    def turn_right(self, ang = 0.3):
        self.msg_pub.angular.z = -ang
    def forward(self, lv=0.3):
        self.msg_pub.linear.x = lv
    def execute(self):
        self.pub.publish(self.msg_pub)
    
    def key_run(self, k):
        self.msg_pub = Twist()
        self.key_input(k)
        self.execute()
    def key_input(self, k):
        if k == 2: self.forward()
        elif k == 6: self.turn_left()
        elif k == 4: self.turn_right()
        elif k == 8: return
        elif k == 7: self.msg_pub.linear.y = 0.3
