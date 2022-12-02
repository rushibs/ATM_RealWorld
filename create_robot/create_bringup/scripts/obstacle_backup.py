#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
# from geometry_msgs.msg import Twist
from std_msgs.msg import Int64 

LINEAR_VEL = 0.1
STOP_DISTANCE = 0.3
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR


def callback(msg):
    global scan
    # scan = LaserScan()
    scan = msg.ranges

    lidar_distances = scan
    min_distance = min(lidar_distances)

    if min_distance < SAFE_STOP_DISTANCE:
        # Obstacle is detected
        rospy.loginfo('Stop!')
    else:
        rospy.loginfo('Distance of the obstacle : %f', min_distance)
           
    print(msg.ranges[0:10])





def main():
    rospy.init_node('obsctacle_node')
    try:
        rospy.Subscriber('scan', LaserScan, callback)
        detect_pub = rospy.Publisher('detect', Int64, queue_size=1)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    # rospy.init_node('obsctacle_node')
    main()
    
    