#!/usr/bin/env python

from cmath import pi
from signal import pause
from struct import calcsize
import rospy
import time
import math
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Twist, Quaternion
from create_msgs.msg import my_msg
from std_msgs.msg import Float64, Int64
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from transfer_data import get_signal

class MovementDetector():
    def __init__(self):
        
        self.flag = 1
        self._current_position = Point()
        self._current_orientation = Quaternion()
        self.velocity = Twist()
        self.mved_distance = my_msg()
        self.turn_angle = my_msg()
        

    
    def get_init_position(self, msg):
  
        try:
    
            self._current_position.x = msg.pose.pose.position.x
            self._current_position.y = msg.pose.pose.position.y
            self._current_position.z = msg.pose.pose.position.z
            self._current_orientation.x = msg.pose.pose.orientation.x
            self._current_orientation.y = msg.pose.pose.orientation.y
            self._current_orientation.z = msg.pose.pose.orientation.z 
            self._current_orientation.w = msg.pose.pose.orientation.w 
            self.mved_distance.distance = 0.0
                      
        except:
            rospy.loginfo("Current odom not ready yet, retrying for setting up init pose")

            
    
    def odom_callback(self, msg):

        rate = rospy.Rate(99999)

        if self.flag == 2:
            NewPosition = msg.pose.pose.position
            NewOrientation = msg.pose.pose.orientation
            self.mved_distance.distance += self.calculate_distance(NewPosition, self._current_position)
            self.turn_angle.angle += self.calculate_angle(NewOrientation, self._current_orientation)
            self.moved_pub = rospy.Publisher('/mved_distance', my_msg, queue_size=10)
            self.moved_pub.publish(self.mved_distance.distance, self.turn_angle.angle) 
            self.updatecurrent_positin(NewPosition)
            self.updatecurrent_orientation(NewOrientation)
            
            
        elif self.flag == 1:
            self.get_init_position(msg)
            self.flag = 2

        rate.sleep()

    def updatecurrent_positin(self, new_position):
        self._current_position.x = new_position.x
        self._current_position.y = new_position.y
        self._current_position.z = new_position.z

        
    def updatecurrent_orientation(self, new_orientation):
        self._current_orientation.x = new_orientation.x
        self._current_orientation.y = new_orientation.y
        self._current_orientation.z = new_orientation.z
        self._current_orientation.w = new_orientation.w


    def calculate_distance(self, new_position, old_position):
        x2 = new_position.x
        y2 = new_position.y
        x1 = old_position.x
        y1 = old_position.y
        dist = math.hypot(x2 - x1, y2 - y1)
        return dist

    def quaternion_to_euler(self, orientation_q):
        
        global roll, pitch, yaw
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        
        return yaw
    
    def calculate_angle(self, new_orientation, old_orientation):
        yaw2 = (self.quaternion_to_euler(new_orientation)) 
        yaw1 = (self.quaternion_to_euler(old_orientation)) 
        angle = abs(abs(yaw2) - abs(yaw1))
        
        return angle

    
    def publish_moved_distance(self, mved_distance, turn_angle):
        None

    # def obstacle_callback():
    #     obs_detect = Int64()
    #     action = obs_detect.data
    #     if action == 1:
    #         print('Obstacle ahead')
    #     elif action == 0:
    #         print('Move')
 


movement_detector = MovementDetector()
        

if __name__ == '__main__':
    rospy.init_node('movement_detector_node', anonymous=True)
    
    rospy.Subscriber("/odom", Odometry, movement_detector.odom_callback)
    # rospy.Subscriber("/detect", Int64, movement_detector.obstacle_callback)
    
    rospy.spin()