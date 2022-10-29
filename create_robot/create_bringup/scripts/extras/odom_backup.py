#!/usr/bin/env python3

from cmath import pi
from signal import pause
from struct import calcsize
import rospy
import time
import math
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Twist, Quaternion
from create_msgs.msg import my_msg
# from geometry_msgs.msg import Twist
# from geometry_msgs.msg import Quaternion
from std_msgs.msg import Float64
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class MovementDetector():
    def __init__(self):
        # print("inside init")
        
        self.flag = 1
        # self.get_init_position()
        self._current_position = Point()
        self._current_orientation = Quaternion()
        self.velocity = Twist()
        self.mved_distance = my_msg()
        self.turn_angle = my_msg()
        


        # self.distance_moved_pub = rospy.Publisher('/mved_distance', Float64, queue_size=10)
        # self.angle_turned_pub = rospy.Publisher('/mved_angle', Float64, queue_size=10)
        # self.velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        # rospy.Subscriber("/odom", Odometry, self.odom_callback)
        # rospy.spin()


    
    def get_init_position(self, msg):
        # data_odom = None
        # while data_odom is None:
        # print("iside get init")
        try:
            # print("try")
            # data_odom = rospy.wait_for_message('/odom', Odometry)
            # self._current_position = Point()
            self._current_position.x = msg.pose.pose.position.x
            self._current_position.y = msg.pose.pose.position.y
            self._current_position.z = msg.pose.pose.position.z
            self._current_orientation.x = msg.pose.pose.orientation.x
            self._current_orientation.y = msg.pose.pose.orientation.y
            self._current_orientation.z = msg.pose.pose.orientation.z 
            self._current_orientation.w = msg.pose.pose.orientation.w 
            self.mved_distance.distance = 0.0
            self.turn_angle.angle = 0.0
            # print("printing")
            
        except:
            rospy.loginfo("Current odom not ready yet, retrying for setting up init pose")

        # self._current_position = Point()
        # self._current_position.x = data_odom.pose.pose.position.x
        # self._current_position.y = data_odom.pose.pose.position.y
        # self._current_position.z = data_odom.pose.pose.position.z 
        # print("printing")
            
    
    def odom_callback(self, msg):
        # print("in callback")

        if self.flag == 2:
            # print("run afterwards")
            NewPosition = msg.pose.pose.position
            NewOrientation = msg.pose.pose.orientation
            # self.mved_distance.data += self.calculate_distance(NewPosition, self._current_position)
            self.mved_distance.distance += self.calculate_distance(NewPosition, self._current_position)
            self.turn_angle.angle += self.calculate_angle(NewOrientation, self._current_orientation)
            # dist = self.mved_distance.distance
            # ang = self.turn_angle.angle
            # self.publish_moved_distance(dist, ang)


            # print('dist = ', self.mved_distance)
            # print("angle = ", self.turn_angle)
            # if self.mved_distance.data >= 0.25 or self.turn_angle.data >= 0.174532925 :
            # if self.mved_distance.data >= 0.25 or self.turn_angle.data >= 10 :    
            #     print("okay")
                # linear_vel = 0.0
                # angular_vel = 0.0
                # self.velocity_pub.Publish(linear_vel)
                # self.velocity_pub.Publish(angular_vel)

            self.moved_pub = rospy.Publisher('/mved_distance', my_msg, queue_size=10)
            # self.angle_turned_pub = rospy.Publisher('/mved_distance', my_msg, queue_size=10)
            self.moved_pub.publish(self.mved_distance.distance, self.turn_angle.angle)
            # self.angle_turned_pub.publish()

            # else:
            #     None
            self.updatecurrent_positin(NewPosition)
            self.updatecurrent_orientation(NewOrientation)
            
            # if self.mved_distance.data < 0.000001 or self.turn_angle.data < 0.00001:
            #     aux1 = Float64()
            #     aux2 = Float64()
            #     aux1.data = 0.0
            #     aux2.data = 0.0
            #     self.distance_moved_pub.publish(aux1)
            #     self.angle_turned_pub.publish(aux2)

            # else:
            #     self.distance_moved_pub.publish(self.mved_distance)

            
        elif self.flag == 1:
            # print('run once')
            self.get_init_position(msg)
            self.flag = 2
    

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
        # orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        # print(yaw)
        return yaw
    
    def calculate_angle(self, new_orientation, old_orientation):
        # roll2 = new_orientation.x
        # pitch2 = new_orientation.y
        yaw2 = (self.quaternion_to_euler(new_orientation)) 
        # print("yaw2 = ", yaw2)
        # roll1 = old_orientation.x
        # pitch1 = old_orientation.y
        yaw1 = (self.quaternion_to_euler(old_orientation)) 
        # print("yaw1 = ", yaw1)
        angle = abs(abs(yaw2) - abs(yaw1))
        # angle = yaw2 - yaw1
        return angle

    
    def publish_moved_distance(self, mved_distance, turn_angle):
        None
        # self.moved_pub = rospy.Publisher('/mved_distance', my_msg, queue_size=10)
        # self.moved_pub.publish(self.mved_distance.distance, self.turn_angle.angle)
       



movement_detector = MovementDetector()
        

if __name__ == '__main__':
    rospy.init_node('movement_detector_node', anonymous=True)
    # MovementDetector()
    rospy.Subscriber("/odom", Odometry, movement_detector.odom_callback)
    
    rospy.spin()