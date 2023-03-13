#!/usr/bin/env python

#python3 -m pip install paramiko
#sudo pip3 install pstats

import paramiko
import time
import os
import csv
# from cryptography.utils import CryptographyDeprecationWarning

##### RUN THIS TO MOUNT THE SERVER STORAGE ON JETSON
###    sudo umount ATM_data 
###    sshfs atm@172.22.136.37:/home/atm ~/ATM_data

#### function to transfer the image captured, from Jetson to PC and deleting the image from Jetson


def transfer_image(frame):
    start_time = time.time()
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()  #####
    # ssh.connect(hostname='10.18.32.227', username='rushi', password='3596', port=22)
    # ssh.connect(hostname='128.238.25.12', username='rs7236', password='1c507!k7P', port=22)

    # tr = ssh.get_transport()
    # tr.default_max_packet_size = 100000000
    # tr.default_window_size = 100000000

    sftp_client = ssh.open_sftp()

    # sftp_client.put('/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/test.jpeg', '/home/rushi/frame_%d.jpeg' %frame)
    sftp_client.put('/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/test.jpeg', '/home/rs7236/ATM/imgs/frame_%d.jpeg' %frame) 
    # sftp_client.get('/home/rushi/a.jpeg', '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/a.jpeg')

    # os.remove('/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/test.jpeg')


    print('done')
    print("--- %s seconds ---" % (time.time() - start_time))
    sftp_client.close()
    ssh.close()


def obs_instruction(ins,index):
    # start_time = time.time()
    
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(hostname='10.18.32.227', username='rushi', password='3596', port=22)
    # ssh.connect(hostname='128.238.25.12', username='rs7236', password='1c507!k7P', port=22)

    # sftp_client = ssh.open_sftp()

    # sftp_client = ssh.open_sftp()

    # sftp_client.open('/home/rs7236/ATM/obs_instructions.txt', 'w+')

    if index == 0:
    
        # with sftp_client.open('/home/rs7236/ATM/obs_instructions.txt', 'w') as f:
        with open('/home/ai4ce/ATM_data/ATM/obs_instructions.txt', 'w') as f:
            # f.prefetch()
            # f.truncate()
            # list = [ins]
            # writer = csv.writer(f)
            # writer.writerow(list)
            ins = str(ins)
            f.write(ins+"\n")
    else:
        # with sftp_client.open('/home/rs7236/ATM/obs_instructions.txt', 'a') as f:
        with open('/home/ai4ce/ATM_data/ATM/obs_instructions.txt', 'a') as f:
        # ncfile = sftp_client.open('mynetCDFfile')
            # f.prefetch()
            # list = [ins]
            # writer = csv.writer(f)
            # writer.writerow(list)
            ins = str(ins)
            f.write(ins+"\n")
    index += 1
    # print('done')
    # print("--- %s seconds ---" % (time.time() - start_time))


    # sftp_client.close()
    # ssh.close()
    
    return index


##### Function to read the actuation command from the last line of the csv file

def get_signal():
    myfilepath = '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/instructions.csv'

    f1 = open(myfilepath, "r")
    signal = f1.readlines()[-1]
    # print(ins)
 
    f1.close()

    return signal

#### Function to write to the 'captured.txt' file that the image has been captured
def obs_flag():
    myfilepath = '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/captured_flags.txt'

    f1 = open(myfilepath, "r")
    
    flag = f1.readlines()[-1]
    # print(ins)

    f1.close()

    return flag

### Function to set obs_flag to zero
def set_obs_flag():
    myfilepath = '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/captured_flags.txt'
    with open(myfilepath, 'a+') as f:
            f.write("0\n")



#### Function to write to 'captured.txt' that an image has ben captured
def captured_flag(captured, frame):

    myfilepath = '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/captured_flags.txt'
    captured = str(captured)
    if frame == 0:
        with open(myfilepath, 'w') as f:
            f.write(captured+"\n")
    else:
        with open(myfilepath, 'a+') as f:
            f.write(captured+"\n")

    f.close()


def stop_bot():
    stop = [0]
    myfilepath = '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/instructions.csv'
    with open(myfilepath, 'a+') as f:
        signal = f.readlines()[-1]
        if int(signal) != 0:
            w = csv.writer(f)
            w.writerow(stop)

    f.close()

# stop_bot() 

