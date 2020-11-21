#!/usr/bin/env python

import rospy
import serial
import time

from time import sleep
from ar_track_alvar_msgs.msg import AlvarMarkers

baud_rate = 115200
port_num = "/dev/ttyUSB0"

ar_port = serial.Serial(port=port_num, baudrate=baud_rate)

time.sleep(0.5)
ar_port.write("$READY\r\n")
print "$READY\r\n"
time.sleep(0.5)

def convert_id(id):
    if id == 10:
        marker_id = 'S'
    elif id == 11:
        marker_id = 'B'
    elif id == 12:
        marker_id = 'C'
    elif id == 13:
        marker_id = 'A'
    else:
        marker_id = str(id)

    return marker_id

def callback(msg):
    time.sleep(0.1)
    time_stamp_signal = 'X'+'\r\n'
    ar_port.write(time_stamp_signal)
    print time_stamp_signal

    for each in msg.markers:
        marker_id = convert_id(int(each.id))
        x_pos = int(each.pose.pose.position.x*1000)
        y_pos = int(each.pose.pose.position.y*1000)
        send_result = "$"+marker_id+","+str(x_pos)+","+str(y_pos)+'\r\n'

        print send_result
        ar_port.write(send_result)

rospy.init_node('get_marker_position')
sub = rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)

rospy.spin()
