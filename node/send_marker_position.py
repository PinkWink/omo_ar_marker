#!/usr/bin/env python

import rospy
import serial
import time

from time import sleep
from ar_track_alvar_msgs.msg import AlvarMarkers

baud_rate = 115200
port = "/dev/ttyTHS1"

# prrospy.get_param('~port')

ar_port = serial.Serial(port=port, baudrate=baud_rate)

time.sleep(0.5)
ar_port.write("$READY\r")
time.sleep(1)

def callback(msg):
    time.sleep(0.1)
    wait_signal = "-"  + '\n\r'
    print wait_signal
    ar_port.write(wait_signal)
    
    for each in msg.markers:
        marker_id = int(each.id)
        x_pos = int(each.pose.pose.position.x*1000)
        y_pos = int(each.pose.pose.position.y*1000)
        # send_result = 'id:' + str(marker_id) + ', ' + 'x:' + str(x_pos) + ', ' + 'y:' + str(y_pos) + '\n\r'
        send_result = "$"+str(marker_id)+","+str(x_pos)+","+str(y_pos)+'\n\r'
        print send_result
        # time.sleep(0.1)
        ar_port.write(send_result)

rospy.init_node('get_marker_position')
sub = rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)

rospy.spin()
