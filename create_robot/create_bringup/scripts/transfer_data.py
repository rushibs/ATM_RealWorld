#!/usr/bin/env python

#python3 -m pip install paramiko
#sudo pip3 install pstats

import paramiko
import time
import os
import csv
# from cryptography.utils import CryptographyDeprecationWarning

#### function to transfer the image captured, from Jetson to PC and deleting the image from Jetson

def transfer_image(frame):
    start_time = time.time()
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.18.32.227', username='rushi', password='3596', port=22)

    sftp_client = ssh.open_sftp()

    sftp_client.put('/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/test.jpeg', '/home/rushi/frame_%d.jpeg' %frame) 
    # sftp_client.get('/home/rushi/a.jpeg', '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/a.jpeg')

    os.remove('/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/test.jpeg')


    print('done')
    print("--- %s seconds ---" % (time.time() - start_time))
    sftp_client.close()
    ssh.close()


##### Function to read the actuation command from the last line of the csv file

def get_signal():
    myfilepath = '/home/ai4ce/instructions.csv'

    f1 = open(myfilepath, "r")
    signal = f1.readlines()[-1]
    # print(ins)
 
    f1.close()

    return signal


def stop_bot():
    stop = [0]
    myfilepath = '/home/ai4ce/instructions.csv'
    with open(myfilepath, 'a') as f:
        w = csv.writer(f)
        w.writerow(stop)

    f.close()

# stop_bot() 

