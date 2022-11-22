#!/usr/bin/env python3
# Import only if not previously imported
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
count = 0

class RosNode:
    def __init__(self):
        rospy.init_node("ros_cam_node")
        rospy.loginfo("Starting RosNode.")
        self.pub = rospy.Publisher("Image_360", Image, queue_size=10)
        self.rate = rospy.Rate(100)
        # self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture("rtmp://192.168.43.1:1935/live/preview")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)
        pass
        

if __name__ == "__main__":
    # print('inside main')
    ros_node = RosNode()
    
    while not rospy.is_shutdown():
        ret, frame = ros_node.cap.read()
        if ret:
            cv2.imshow("frame", frame)
            bridge = CvBridge()
            cv_image = bridge.cv2_to_imgmsg(frame, "bgr8")

            ros_node.pub.publish(cv_image)
            ros_node.rate.sleep()
            # if cv2.waitKey(20) & 0xFF == 27:
            #     break
            if cv2.waitKey(33) == ord('0'):
                print ("Capturing Frame")
                cv2.imwrite("/home/rushi/create_ws/src/create_robot/create_bringup/scripts/data_new/image_%d.png" % count, frame)
                count +=1
                print(count)
    # rospy.spin()
    