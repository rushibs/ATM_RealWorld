#!/usr/bin/env python2

# from json import detect_encoding
import threading
import time
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
from std_msgs.msg import Float64, Int64
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
from create_msgs.msg import my_msg
from camera import capture, check_state, connect
from transfer_data import transfer_image, get_signal, stop_bot

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty
import cv2

TwistMsg = Twist

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    odef obstacle_callback():
    obs_detect = Int64()
    action = obs_detect.data
    if action == 1:
        print('Obstacle ahead')
    elif action == 0:
        print('Move')
   j    k    l
   m    ,    .
For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >
t : up (+z)
b : down (-z)
anything else : stop
q/z : increase/decrease max speeds by 10%def obstacle_callback():
    obs_detect = Int64()
    action = obs_detect.data
    if action == 1:
        print('Obstacle ahead')
    elif action == 0:
        print('Move')
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
CTRL-C to quit
"""

moveBindings = {
        '3':(1,0,0,0),     #forward
        'o':(1,0,0,-1),
        '1':(0,0,0,1),     #left
        '2':(0,0,0,-1),    #right
        'u':(1,0,0,1),
        '4':(-1,0,0,0),    #back
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }

move_signals = {3:[1,0,0,0]}

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }


class PublishThread(threading.Thread):
    def __init__(self, rate):
        
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('cmd_vel', TwistMsg, queue_size = 1)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()
    

    def run(self):
        print("i'm here")
        twist_msg = TwistMsg()
        
        if stamped:
            twist = twist_msg.twist
            twist_msg.header.stamp = rospy.Time.now()
            twist_msg.header.frame_id = twist_frame
        else:
            twist = twist_msg
        while not self.done:
            if stamped:
                twist_msg.header.stamp = rospy.Time.now()
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish
            
            self.publisher.publish(twist_msg)

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist_msg)


def getKey(settings, timeout):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

pose = 0.0
turn_angle = 0.0
frame = 0

def odom_callback(msg):
    global pose, turn_angle, frame, signal
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
    twist_msg2 = TwistMsg()
    distance = my_msg()
    angle = my_msg()
    dist = msg.distance
    ang = msg.angle


    if dist >= (pose+0.25): 
        stop_bot()
        if signal != 0:
            header = connect()
            print("Capture Image")
            t_end = time.time() + 60 * 0.05
            while time.time() < t_end:
                twist_msg2.linear.x = 0
                twist_msg2.angular.z = 0
                publisher.publish(twist_msg2)
            
            pose = dist
            capture(header)
            print('transferring image')
            transfer_image(frame)
            frame+=1
            print('done')
            time.sleep(7.5)
            print('next')
   


    if ang >= (turn_angle+0.174532925):
        stop_bot()
        if signal != 0:
            header = connect()
            print("Capture Image")
            t_end = time.time() + 60 * 0.05
            while time.time() < t_end:
                twist_msg2.linear.x = 0
                twist_msg2.angular.z = 0
                publisher.publish(twist_msg2)
            turn_angle = ang
            capture(header)
            print('transferring image')
            transfer_image(frame)
            frame+=1
            print('done')
            time.sleep(7.5)
            print('next')
          
            

# def obstacle_callback(data):
#     print(data)
    # obs_detect = Int64()
    # action = obs_detect.data
    
    # if action == 1:
    #     print('Obstacle ahead')
    # elif action == 0:
    #     print('Move')

def sub_node():
    
    rospy.Subscriber("/mved_distance", my_msg, odom_callback)
    # rospy.Subscriber("/detect", Int64, obstacle_callback)


if __name__=="__main__":
    
    settings = saveTerminalSettings()
    rospy.init_node('teleop_twist_keyboard1')
    speed = rospy.get_param("~speed", 0.1)
    turn = rospy.get_param("~turn", 1.0)
    repeat = rospy.get_param("~repeat_rate", 10.0)
    key_timeout = rospy.get_param("~key_timeout", 0.5)
    stamped = rospy.get_param("~stamped", False)
    twist_frame = rospy.get_param("~frame_id", '')
    if stamped:
        TwistMsg = TwistStamped

    pub_thread = PublishThread(repeat)

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0
    
    
    
    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(x, y, z, th, speed, turn)

        print(msg)
        print(vels(speed,turn))
        
        start = 1
        
        while(1):
            key = getKey(settings, key_timeout)       

            while(start == 1):                      ###### Switch to turn on the bot
                start = input('Press 0 to start ') 
         
            
            signal = get_signal()                   ###### read signal from csv file
            
            if int(signal)==3:
                x = 1
                y = 0
                z = 0
                th = 0   
            elif int(signal)==1:
                
                x = 0
                y = 0
                z = 0
                th = 1
            elif int(signal)==2:
                x = 0
                y = 0
                z = 0
                th = -1
            elif key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]

            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]

                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                x = 0
                y = 0
                z = 0
                th = 0
            
            
            if (key == '\x03'):
                break

            pub_thread.update(x, y, z, th, speed, turn)
            sub_node()


    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        restoreTerminalSettings(settings)