#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64 
import time
from create_msgs.msg import my_msg

pose = 0.0
turn_angle = 0.0
def odom_callback(msg):
    global pose, turn_angle
    distance = my_msg()
    angle = my_msg()
    dist = msg.distance
    ang = msg.angle
    if dist >= (pose+0.25): 
        # print("dist = ", dist)
        print("Capture Image")
        pose = dist
    
    if ang >= (turn_angle+0.174532925):
        # print("angle = ", ang)
        print("Capture Image")
        turn_angle = ang


def sub_node():
    rospy.init_node("sub_node", anonymous=True)
    rospy.Subscriber("/mved_distance", my_msg, odom_callback)
 
    rospy.spin()

if __name__ == "__main__":
    sub_node()
    