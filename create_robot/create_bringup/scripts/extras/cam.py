#!/usr/bin/env python3

import cv2# In VideoCaptur object either Pass address of your Video file# Or If the input is the camera, pass 0 instead of the video file
cap = cv2.VideoCapture("rtmp://192.168.43.1:1935/live/preview")
#print(cap)
#cap.set(cv2.CAP_PROP_FPS, 5)

if cap.isOpened() == False:
    print("Error in opening video stream or file")
count = 0

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer= cv2.VideoWriter('/home/rushi/create_ws/src/create_robot/create_bringup/scripts/test.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        fps = int(cap.get(30))
        print("fps:", fps)
        # Display the resulting frame
        writer.write(frame)
        cv2.imshow('Frame',frame)
        cv2.imwrite("/home/rushi/create_ws/src/create_robot/create_bringup/scripts/data/image_%d.png" % count, frame)
        count+=1
        # Press esc to exit
        if cv2.waitKey(20) & 0xFF == 27:
            break
    else:
        break
cap.release()
writer.release()
cv2.destroyAllWindows()
