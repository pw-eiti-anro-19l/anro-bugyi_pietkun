#!/usr/bin/env python

import sys
import rospy
from zadanie31.srv import *
from std_msgs.msg import String


def oint_client(px, py, pz ,x,y,z,roll,pitch,yaw,t,typ):
    rospy.wait_for_service('oint_control_srv')
    try:
        oint_control_srv = rospy.ServiceProxy('oint_control_srv', oint)
        resp1 = oint_control_srv(px,py,pz,x,y,z,roll,pitch,yaw,t,typ)
        return resp1.status
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [px py pz x y z roll pitch yaw t typ]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 12:
        px = float(sys.argv[1])
        py = float(sys.argv[2])
        pz = float(sys.argv[3])
	x = float(sys.argv[4])
        y = float(sys.argv[5])
        z = float(sys.argv[6])
        roll = float(sys.argv[7])
        pitch = float(sys.argv[8])
        yaw = float(sys.argv[9])
        t = float(sys.argv[10])
        typ = str(sys.argv[11])
    else:
        print usage()
        sys.exit(1)
    print "Requesting params: %s %s %s %s %s %s %s %s %s %s %s"%(px,py,pz,x,y,z,roll,pitch,yaw,t,typ)
    print "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s -> %s"%(px,py,pz,x,y,z,roll,pitch,yaw,t,typ, oint_client(px,py,pz,x,y,z,roll,pitch,yaw,t,typ))
