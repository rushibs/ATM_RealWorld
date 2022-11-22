import pandas as pd

df = pd.read_csv('/home/ai4ce/create_ws/src/data/odom.csv', index_col=False)
df['index'] = df.index
selected_columns = ["index", "field.header.seq", "field.header.stamp", "field.pose.pose.position.x", "field.pose.pose.position.y", 
                    "field.pose.pose.position.z", "field.pose.pose.orientation.x", "field.pose.pose.orientation.y", "field.pose.pose.orientation.z"]

df = df[selected_columns]

df.to_csv('/home/ai4ce/create_ws/src/data/output_odom.csv', index=False)