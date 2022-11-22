#!/usr/bin/env python3

### RUN THESE IN TERMINAL BEFORE RUNNING THE FILE

## rostopic echo /odom -b /media/rushi/sarthak/data/odom.bag -p > /media/rushi/sarthak/data/odom.csv

## rostopic echo /velodyne_points -b /media/rushi/sarthak/data/pcd.bag -p > /home/rushi/data/pcd.csv

## rosrun pcl_ros bag_to_pcd /media/rushi/sarthak/data/pcd.bag velodyne_points /home/rushi/data/lidar_data

import os
import pandas as pd

#########RENAME THE LIDAR DATA##############################


# folder = r'/home/rushi/data/lidar_data/'
# count = 0

# for file_name in os.listdir(folder):
#     source = folder + file_name

#     destination = folder + str(count) + ".pcd"

#     os.rename(source, destination)
#     count+=1

# print('All files renamed')


############EXTRACT ODOM#####################

df = pd.read_csv('/media/rushi/sarthak/data/odom.csv', index_col=False)
df['index'] = df.index
selected_columns = ["index", "field.header.seq", "field.header.stamp", "field.pose.pose.position.x", "field.pose.pose.position.y", 
                    "field.pose.pose.position.z", "field.pose.pose.orientation.x", "field.pose.pose.orientation.y", "field.pose.pose.orientation.z"]

df = df[selected_columns]

df.to_csv('/home/rushi/data/output_odom.csv', index=False)

