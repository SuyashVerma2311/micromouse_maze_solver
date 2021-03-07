import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import numpy as np

class Controller(object):
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.current_state = [0, 0] # velocity, direction
        self.target_state = self.current_state
        self.msg_pub = None
        self.state = None
        self.velocity = 0.2

    def run(self, state_, cmd):
        self.state = state_
        if cmd != self.target_state[1]: 
            self.target_state[1] = cmd*90
        self.adjust()


        self.msg_pub = Twist()
        

    def key_run(self, k):
        self.msg_pub = Twist()
        self.key_input(k)
        self.execute()

    

    def adjust(self):
        if abs(self.target_state[1] - self.current_state[1]) < 5:
            return
        diff = self.target_state[1] - self.current_state[1]
        
        
        

    def turn_left(self, ang = 0.3):
        self.msg_pub.angular.z = ang
    def turn_right(self, ang = 0.3):
        self.msg_pub.angular.z = -ang
    def forward(self):
        self.msg_pub.linear.x = self.velocity
    def rotate180(self):
        pass
    def execute(self):
        self.pub.publish(self.msg_pub)
    def key_input(self, k):
        if k == 2: self.forward()
        elif k == 6: self.turn_left()
        elif k == 4: self.turn_right()
        elif k == 8: self.rotate180()
        




