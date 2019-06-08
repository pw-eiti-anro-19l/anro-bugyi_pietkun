#!/usr/bin/env python

import sys
import rospy
import time
from zadanie31.srv import *
from std_msgs.msg import String
from math import *

def oint_client(x,y,z,roll,pitch,yaw,t,typ):
    rospy.wait_for_service('oint_control_srv')
    try:
        oint_control_srv = rospy.ServiceProxy('oint_control_srv', oint)
        resp1 = oint_control_srv(x,y,z,roll,pitch,yaw,t,typ)
        return resp1.status
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y z roll pitch yaw t typ]"%sys.argv[0]

if __name__ == "__main__":
    if float(sys.argv[1]) == 0 :
        oint_client(0.5,0.5,0.5,1,1,1,5,'linear')
        #time.sleep(float(sys.argv[1]))
        oint_client(-0.5,0.5,0.5,1,1,1,5,'linear')
        #time.sleep(float(sys.argv[1]))
        oint_client(-0.5,-0.5,0.5,1,1,1,5,'linear')
        #time.sleep(float(sys.argv[1]))
        oint_client(0.5,-0.5,0.5,1,1,1,5,'linear')
        #time.sleep(float(sys.argv[1]))
        oint_client(0.5,0.5,0.5,1,1,1,5,'linear')
        #time.sleep(float(sys.argv[1]))
    else :
        for i in range(200) :
            oint_client(0.6*cos(i*0.05),0.2*sin(i*0.05),0.5,1,1,1,0.1,'linear')
