#!/usr/bin/env python2

import requests
import json
import time
# import matplotlib.pyplot as plt

# Ethernet connection ipv4 address: 192.168.1.100, mask: 255.255.255.0

# Connecting. 

# Every post you have a parameter and a header
def check_state(header):
        try:
            r = requests.post('http://192.168.1.188:20000/osc/state', headers=header)  ###CHECK FOR r
            time.sleep(2)

        except:
            print("hi")
             

def connect():
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

  connect_response = requests.post('http://192.168.1.188:20000/osc/commands/execute', data=json.dumps(connect_param), headers = connect_header)
  my_fingerprint = connect_response.json()['results']['Fingerprint'] # access token for this specific connection

  ###### connection estbalished

  # You will have to check for state at least once per 10 second. But the maximum speed you can do is 1 check per second
  # check for state. 
  header = {
      "Fingerprint":my_fingerprint,
      "Content-Type":"application/json; charset=utf-8"
  }

  r = requests.post('http://192.168.1.188:20000/osc/state', headers=header)

  return header


def capture(header):  


  check_state(header)

  take_pic_time = time.time()
  # take a pic
  take_pic_param = {
    "name": "camera._takePicture",
    "parameters":{
      "origin":{
        "mime":"jpeg", 
        "width":4000,
        "height":3000,
        "saveOrigin":False,
        "storage_loc":1 
      },
      "stiching":{
        "mode":"pano", 
        "mime":"jpeg", 
        "width":3840, 
        "height":1920, 
        "map":"equirectangular", 
        "algorithm":"normal" 
      },
      "burst":{"enable":False, "count":0},
      "hdr":{"enable":False, "count":0, "min_ev":0, "max_ev":0},
      "bracket":{"enable":False, "count":0, "min_ev":0, "max_ev":0}, 
      "delay":0,
    }
  }


  take_pic_response = requests.post('http://192.168.1.188:20000/osc/commands/execute', data=json.dumps(take_pic_param), headers = header)

  this_img_int = take_pic_response.json()["sequence"] #the id of your pic
  get_result_param = {
    "name":"camera._getResult",
    "parameters": {
      "list_ids": [this_img_int]
    }
  }

  check_state(header)

  while True:
    state_response = requests.post('http://192.168.1.188:20000/osc/state', headers=header)
    if this_img_int in state_response.json()["state"]["_idRes"]: # the photo is done processing, ready for me to take
      check_state(header)
      result_response = requests.post('http://192.168.1.188:20000/osc/commands/execute', data=json.dumps(get_result_param), headers = header)
      print('total time used: ', time.time()-take_pic_time)
      break
    time.sleep(1)

  check_state(header)
  pic_url = result_response.json()["results"]["res_array"][0]["results"]["results"]["_picUrl"]
  pic_url = 'http://192.168.1.188:8000' + pic_url + '/pano.jpg'


  pic = requests.get(pic_url)

  with open(r'/home/ai4ce/create_ws/src/create_robot/create_bringup/scripts/test.jpeg','wb') as f:
      f.write(pic.content)



###Trial

# for i in range(50):
#   start = time.time()
#   if start < start+10:
#     if i == 0:
#       header = connect()
#     capture(header)
#     i += 1
#   else:
#     header = connect()
#     capture(header)