#!/usr/bin/env python2

#python3 -m pip install paramiko
#sudo pip3 install pstats

import paramiko
import time
import os
from cryptography.utils import CryptographyDeprecationWarning

start_time = time.time()


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='10.18.44.45', username='rushi', password='3596', port=22)

sftp_client = ssh.open_sftp()

sftp_client.put('/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/test.jpeg', '/home/rushi/a.jpeg')

sftp_client.get('/home/rushi/a.jpeg', '/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/a.jpeg')

os.remove('/home/ai4ce/ATM_Jetson/create_robot/create_bringup/scripts/a.jpeg')


print('done')
print("--- %s seconds ---" % (time.time() - start_time))
sftp_client.close()
ssh.close()