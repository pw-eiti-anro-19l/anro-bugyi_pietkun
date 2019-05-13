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
from std_msgs.msg import *


global pub
global uklad
global pub1
global pub2
global pub3
global pub4
global pub5
global pub6


def handle_interpolation(req):
    if (req.time<=0):
        return ointResponse("Niepoprawny czas")

    if (req.type!="linear" and req.type!="trapezoid"):
        return ointResponse("Niepoprawny typ interpolacji")

    xpocz=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]	#poczatkowe wartosci polozenia i orientacji

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
        roll_val=rolll.interpolation(req.type, xpocz[0], req.roll,kkonc,k)
        pitch_val=pitchh.interpolation(req.type, xpocz[1], req.pitch,kkonc,k)
        yaw_val=yaww.interpolation(req.type, xpocz[2], req.yaw,kkonc,k)

        uklad.set_coordinates(x_val,y_val,z_val,roll_val,pitch_val,yaw_val)

        state=uklad.get_pose()
        pub=rospy.Publisher('pose_stamped',PoseStamped,queue_size=10)
        pub.publish(state)

        pub1=rospy.Publisher('x_val',Float64,queue_size=10)
        pub1.publish(x_val)
        pub2=rospy.Publisher('y_val',Float64,queue_size=10)
        pub2.publish(y_val)
        pub3=rospy.Publisher('z_val',Float64,queue_size=10)
        pub3.publish(z_val)
        pub4=rospy.Publisher('roll_val',Float64,queue_size=10)
        pub4.publish(roll_val)
        pub5=rospy.Publisher('pitch_val',Float64,queue_size=10)
        pub5.publish(pitch_val)
        pub6=rospy.Publisher('yaw_val',Float64,queue_size=10)
        pub6.publish(yaw_val)


        k=k+1
        r.sleep()

    return ointResponse('Interpolacja zakonczona')



def oint_server():
    rospy.init_node('oint')
    s = rospy.Service('oint_control_srv', oint, handle_interpolation)
    print "Ready to interpolate."
    pub = rospy.Publisher('/pose_stamped', PoseStamped, queue_size=10)

    init_state=PoseStamped()
    init_state.header.stamp = rospy.Time.now()
    init_state.header.frame_id = 'base_link'
    init_state.pose.position=[0.0, 0.0, 0.0]
    init_state.pose.orientation=[0.0, 0.0, 0.0, 0.0]

    rospy.sleep(0.5)
    pub.publish(init_state)

    #init_state = robot.get_joint_state(0)	    
    rospy.spin()


if __name__ == "__main__":
    uklad = uklad.Uklad()
    oint_server()
