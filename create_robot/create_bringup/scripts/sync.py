#!/usr/bin/env python2

import rospy
import message_filters
import rosbag
from sensor_msgs.msg import PointCloud2
from nav_msgs.msg import Odometry

bag1 = rosbag.Bag('/home/ai4ce/create_ws/src/data/pcd.bag', 'w')
bag2 = rosbag.Bag('/home/ai4ce/create_ws/src/data/odom.bag', 'w')

rospy.init_node('sync_time')
    
def cloud(PointCloud2, Odometry):
    print('store')
    pcd = PointCloud2
    odo = Odometry
    bag1.write('velodyne_points', pcd)
    bag2.write('odom', odo)


lidar_sub = message_filters.Subscriber("/velodyne_points", PointCloud2)
odometry_sub = message_filters.Subscriber("/odom", Odometry)

ats = message_filters.ApproximateTimeSynchronizer([lidar_sub, odometry_sub], queue_size=10, slop=0.05)
ats.registerCallback(cloud)
rospy.spin()
bag1.close()
bag2.close()