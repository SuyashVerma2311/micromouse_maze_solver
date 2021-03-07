import numpy as np
import cv2
from obstacle import Obstacle
from controller import Controller
import rospy

rospy.init_node('test_node')
obj = Obstacle()
car = Controller()
# obj.display()
cv2.namedWindow("Testing", 100)

while not rospy.is_shutdown():
    print(" -- -- ")
    obj.display()
    key = cv2.waitKey(100)
    if key == 27:
        break    
    key = key - 48
    car.key_run(key)
    # rospy.spin()

print("end")
cv2.destroyAllWindows()

