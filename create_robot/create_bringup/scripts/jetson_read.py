import os
import csv
import pandas as pd

df = pd.read_csv('/media/rushi/data/command.csv', index_col=False)

df['index'] = df.index
selected_columns = ["index", "field.header.seq", "field.header.stamp", "field.pose.pose.position.x", "field.pose.pose.position.y", 
                    "field.pose.pose.position.z", "field.pose.pose.orientation.x", "field.pose.pose.orientation.y", "field.pose.pose.orientation.z"]

df = df[selected_columns]

df.to_csv('/home/rushi/data/output_odom.csv', index=False)