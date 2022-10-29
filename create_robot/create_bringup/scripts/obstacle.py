#!/usr/bin/env python3

import rospy
import math
from sensor_msgs.msg import LaserScan
# from geometry_msgs.msg import Twist
from std_msgs.msg import String 

LINEAR_VEL = 0.1
STOP_DISTANCE = 0.3
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR

# class Obstacle():
    # def __init__():
    #     detect = rospy.Publisher('detect', Bool, queue_size=1)

    #     obstacle()

def callback(msg):
    global scan
    scan = LaserScan()
    # scan = msg

    # scan_filter = get_scan(scan)
    # stop = obstacle()
    # detect_pub.publish(stop)
     
    
# def get_data():
#     rospy.Subscriber('scan', LaserScan, callback)

#     rospy.spin()

def get_scan():
    scan = rospy.wait_for_message('scan', LaserScan)
    scan_filter = []
    
    samples = len(scan.ranges)  # The number of samples is defined in 
                                # turtlebot3_<model>.gazebo.xacro file,
                                # the default is 360.
    samples_view = 1            # 1 <= samples_view <= samples
    
    if samples_view > samples:
        samples_view = samples

    if samples_view == 1:
        scan_filter.append(scan.ranges[0])

    else:
        left_lidar_samples_ranges = -(samples_view//2 + samples_view % 2)
        right_lidar_samples_ranges = samples_view//2
        
        left_lidar_samples = scan.ranges[left_lidar_samples_ranges:]
        right_lidar_samples = scan.ranges[:right_lidar_samples_ranges]
        scan_filter.extend(left_lidar_samples + right_lidar_samples)

    for i in range(samples_view):
        if scan_filter[i] == float('Inf'):
            scan_filter[i] = 3.5
        elif math.isnan(scan_filter[i]):
            scan_filter[i] = 0
    
    return scan_filter

def obstacle(scan_filter):
    detect = String()
    detect.data = 'go'

    while not rospy.is_shutdown():
        # lidar_distances = get_scan()
        lidar_distances = scan_filter
        min_distance = min(lidar_distances)
        print(min_distance)
        if min_distance < SAFE_STOP_DISTANCE:
            # if turtlebot_moving:
            detect.data = 'stop'
            # detect.publish(detect)
            # turtlebot_moving = False
            rospy.loginfo('Stop!')
        else:
            # twist.linear.x = LINEAR_VEL
            # twist.angular.z = 0.0
            # _cmd_pub.publish(twist)
            # turtlebot_moving = True
            # rospy.loginfo('Distance of the obstacle : %f', min_distance)
            detect.data = 'go'
    
    return detect


def main():
    rospy.init_node('obsctacle_node')
    try:
        # rospy.Subscriber('scan', LaserScan, callback)
        laser_pub = rospy.Publisher('scan', LaserScan, queue_size=10)
        detect_pub = rospy.Publisher('detect', String, queue_size=5)
        scan_filter = get_scan()
        stop = obstacle(scan_filter)
        detect_pub.publish(stop.data) 

    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()