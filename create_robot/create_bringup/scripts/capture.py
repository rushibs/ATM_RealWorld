

import requests
import json
import time
import cam_check_state
from cam_check_state import header


def capture():
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


    while True:
        state_response = requests.post('http://192.168.1.188:20000/osc/state', headers=header)
            
        if this_img_int in state_response.json()["state"]["_idRes"]: # the photo is done processing, ready for me to take
            result_response = requests.post('http://192.168.1.188:20000/osc/commands/execute', data=json.dumps(get_result_param), headers = header)
            print('total time used: ', time.time()-take_pic_time)
            break
        time.sleep(1)

        pic_url = result_response.json()["results"]["res_array"][0]["results"]["results"]["_picUrl"]
        pic_url = 'http://192.168.1.188:8000' + pic_url + '/pano.jpg'


        pic = requests.get(pic_url)
            
        with open(r'./test.jpeg','wb') as f:
            f.write(pic.content)

    return None

capture()