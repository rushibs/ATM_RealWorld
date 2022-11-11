#!/usr/bin/env python3

#sudo pip3 install pstats

import paramiko
import time
start_time = time.time()


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.0.243', username='ai4ce', password='ai4ce', port=22)

sftp_client = ssh.open_sftp()

sftp_client.get('/media/ai4ce/sarthak/odom.csv', '/home/rushi/trial.csv')
sftp_client.remove('/home/ai4ce/data/a.JPG')

sftp_client.put('/home/rushi/a.JPG', '/home/ai4ce/data/a.JPG')


print('done')
print("--- %s seconds ---" % (time.time() - start_time))
sftp_client.close()
ssh.close()