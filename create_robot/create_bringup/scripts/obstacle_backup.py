#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
# from geometry_msgs.msg import Twist
from std_msgs.msg import Int64 

LINEAR_VEL = 0.1
STOP_DISTANCE = 0.5
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR


def callback(msg):
    global scan
    obstacle_detect = Int64()
    scan = msg.ranges

    lidar_distances = scan
    min_distance = min(lidar_distances)

    detect_pub = rospy.Publisher('detect', Int64, queue_size=1)

    if min_distance < SAFE_STOP_DISTANCE:
        # Obstacle is detected
        # rospy.loginfo('Stop!')
        obstacle_detect.data = 1
        detect_pub.publish(obstacle_detect)

    else:
        obstacle_detect.data = 0
        detect_pub.publish(obstacle_detect)
        # rospy.loginfo('Distance of the obstacle : %f', min_distance)
           
    # print(msg.ranges[0:10])



def main():
    rospy.init_node('obsctacle_node')
    rospy.Subscriber('scan', LaserScan, callback)
  
if __name__ == '__main__':
    main()
    rospy.spin()
    
    