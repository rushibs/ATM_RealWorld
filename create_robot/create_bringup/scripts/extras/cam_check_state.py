#!/usr/bin/env python2

import requests
import json
import time

#Ethernet connection ipv4 address: 192.168.1.100, mask: 255.255.255.0

# Connecting. 

# Every post you have a parameter and a header
while(True):  
    connect_param = {
        "name": "camera._connect",
        "parameters": {
            "hw_time": "MMDDhhmm[[CC]YY][.ss]",
            "time_zone": "EST-05:00/EDT-04:00"
        }
    }

    # header for meta data
    connect_header = {
        "Fingerprint":"",
        "Content-Type":"application/json; charset=utf-8"
    }

    # start = time.time()
    
    connect_response = requests.post('http://192.168.1.188:20000/osc/commands/execute', data=json.dumps(connect_param), headers = connect_header)
    my_fingerprint = connect_response.json()['results']['Fingerprint'] # access token for this specific connection

    ###### connection estbalished

    # You will have to check for state at least once per 10 second. But the maximum speed you can do is 1 check per second
    # check for state. 

    header = {
            "Fingerprint":my_fingerprint,
            "Content-Type":"application/json; charset=utf-8"
        }

    def check_state(header):
        try:
            r = requests.post('http://192.168.1.188:20000/osc/state', headers=header)  ###CHECK FOR r
            time.sleep(2)

        except:
            print("hi")
            break 
        
        # if  header["Fingerprint"] == my_fingerprint:    
        #     time.sleep(2)
        # else:
        #     break
