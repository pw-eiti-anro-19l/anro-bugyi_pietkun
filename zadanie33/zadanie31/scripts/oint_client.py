#!/usr/bin/env python

import sys
import rospy
from zadanie31.srv import *
from std_msgs.msg import String


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
    if len(sys.argv) == 9:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        z = float(sys.argv[3])
        roll = float(sys.argv[4])
        pitch = float(sys.argv[5])
        yaw = float(sys.argv[6])
        t = float(sys.argv[7])
        typ = str(sys.argv[8])
    else:
        print usage()
        sys.exit(1)
    print "Requesting params: %s %s %s %s %s %s %s %s"%(x,y,z,roll,pitch,yaw,t,typ)
    print "%s, %s, %s, %s, %s, %s, %s, %s -> %s"%(x,y,z,roll,pitch,yaw,t,typ, oint_client(x,y,z,roll,pitch,yaw,t,typ))
