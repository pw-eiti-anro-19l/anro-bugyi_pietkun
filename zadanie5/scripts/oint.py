#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import *
from tf.transformations import *
import uklad
from interpolators import JINT
from zadanie31.srv import *
from nav_msgs.msg import *


global pub
global uklad
xpocz=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]	#poczatkowe wartosci polozenia i orientacji
pth=Path()

def handle_interpolation(req):
    if (req.time<=0):
        return ointResponse("Niepoprawny czas")

    if (req.type!="linear" and req.type!="trapezoid"):
        return ointResponse("Niepoprawny typ interpolacji")

    f=100			#czestotliwosc probkowania
    r=rospy.Rate(f)
    k=0				#chwila poczatkowa
    kkonc=f*req.time		#chwila koncowa

    xx=JINT()
    yy=JINT()
    zz=JINT()
    rolll=JINT()
    pitchh=JINT()
    yaww=JINT()



    while k<=kkonc:

        x_val=xx.interpolation(req.type, xpocz[0], req.x,kkonc,k)
        y_val=yy.interpolation(req.type, xpocz[1], req.y,kkonc,k)
        z_val=zz.interpolation(req.type, xpocz[2], req.z,kkonc,k)
        roll_val=rolll.interpolation(req.type, xpocz[3], req.roll,kkonc,k)
        pitch_val=pitchh.interpolation(req.type, xpocz[4], req.pitch,kkonc,k)
        yaw_val=yaww.interpolation(req.type, xpocz[5], req.yaw,kkonc,k)

        uklad.set_coordinates(x_val,y_val,z_val,roll_val,pitch_val,yaw_val)

        state=uklad.get_pose()
        pub=rospy.Publisher('pose_stamped',PoseStamped,queue_size=10)
        pub.publish(state)
	pub1=rospy.Publisher('path',Path,queue_size=10)
        
        pub.publish(state)
        pth.header = state.header
        pth.poses.append(state)
        pub1.publish(pth)
        
        k=k+1
        r.sleep()

    xpocz[0]=x_val
    xpocz[1]=y_val
    xpocz[2]=z_val
    xpocz[3]=roll_val
    xpocz[4]=pitch_val
    xpocz[5]=yaw_val

    return ointResponse('Interpolacja zakonczona')



def oint_server():
    rospy.init_node('oint')
    s = rospy.Service('oint_control_srv', oint, handle_interpolation)
    print "Ready to interpolate."
    pub = rospy.Publisher('/pose_stamped', PoseStamped, queue_size=10)

    init_state=PoseStamped()
    init_state.header.stamp = rospy.Time.now()
    init_state.header.frame_id = 'base_link'
    init_state.pose.position.x=0
    init_state.pose.position.y=0
    init_state.pose.position.z=0
    init_state.pose.orientation.x=0
    init_state.pose.orientation.y=0
    init_state.pose.orientation.z=0
    init_state.pose.orientation.w=0

    rospy.sleep(0.5)

    #init_state = robot.get_joint_state(0)	    
    rospy.spin()


if __name__ == "__main__":
    uklad = uklad.Uklad()
    oint_server()
