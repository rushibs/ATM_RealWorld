#!/usr/bin/env python
# from socket import MsgFlag
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Point, Quaternion
import cv2
import keyboard

class ROSNode:
    def __init__(self):
        rospy.init_node("name_node")
        rospy.loginfo("Starting ROSNode as name_node.")
        self.sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.message_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.rate = 10
        
        pass
    
    def odom_callback(self, msg):
        
            pos = msg.pose.pose.position.x
            self.msg_pub = Twist()
            pose = 0
            if keyboard.read_key("w"):
                print("hello")
                if pos <= (pose+ 0.25):
                    self.msg_pub.linear.x = 0.05
                    self.message_pub.publish(self.msg_pub)
                    # rospy.Rate(10)  
                else:
                    self.msg_pub.linear.x = 0.0
                    self.message_pub.publish(self.msg_pub)
        


if __name__ == "__main__":
    name_node = ROSNode()
    rospy.spin()
    