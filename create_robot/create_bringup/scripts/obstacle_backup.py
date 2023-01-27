#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
# from geometry_msgs.msg import Twist
from std_msgs.msg import Int64 
from transfer_data import obs_instruction
from transfer_data import obs_flag, captured_flag, set_obs_flag

LINEAR_VEL = 0.1
STOP_DISTANCE = 0.7
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR

# obs_flag = Int64()
# obs_flag = 0

# def obs_callback(msg):

#     obs_flag = msg.data
#     print('msg data', obs_flag)
#     obs_pub = rospy.Publisher('obs_int', Int64, queue_size=10)
#     msg.data = 0
#     obs_pub.publish(msg)
        
        

index = 0
def callback(msg):
    global index, scan

    obstacle_detect = Int64()
    scan = msg.ranges
    lidar_distances = scan
    # lidar_distances = scan[448:597]
    min_distance = min(lidar_distances)



    detect_pub = rospy.Publisher('detect', Int64, queue_size=1)
    # rospy.Subscriber('obs_int', Int64, obs_callback)


    if min_distance < SAFE_STOP_DISTANCE:
        # Obstacle is detected
        # rospy.loginfo('Stop ! Distance of the obstacle : %f', min_distance)

        flag = obs_flag()
        flag = int(flag)
        obstacle_detect.data = 1
        # print('global variable', obs_flag)
        
        if flag == 1:
            ins = 1                   #### Detection for an obstacle (detected)
            index = obs_instruction(ins, index)
            set_obs_flag()
        detect_pub.publish(obstacle_detect)

    else:

        flag = obs_flag()
        flag = int(flag)
        obstacle_detect.data = 0
        # print('global variable', obs_flag)
        if flag == 1:
            ins = 0                 #### Detection for an obstacle (Not detected)
            index = obs_instruction(ins, index)
            set_obs_flag()
        detect_pub.publish(obstacle_detect)
        # rospy.loginfo('Distance of the obstacle : %f', min_distance)
           
    # print(len(msg.ranges[:]))



def main():
    rospy.init_node('obsctacle_node')
    rospy.Subscriber('scan', LaserScan, callback)
    # rospy.Subscriber('obs_int', Int64, obs_callback)
  
if __name__ == '__main__':
    main()
    rospy.spin()
    
    