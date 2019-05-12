#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import *
from tf.transformations import *
import robot
from interpolators import JINT
from zadanie31.srv import *
from nav_msgs.msg import *###

global path_pub###
global pub
global robot


def handle_interpolation(req):
    if (req.time<=0):
        return jintResponse("Niepoprawny czas")

    if (req.j1>1.5 or req.j1<-1.5 or req.j2>1.5 or req.j2<-1.5 or req.grip>0.3 or req.grip<0):
        return jintResponse("Niepoprawne parametry")

    if (req.type!="linear" and req.type!="trapezoid"):
        return jintResponse("Niepoprawny typ interpolacji")

    xpocz=[0.0, 0.0, 0.0]	#poczatkowe wartosci na stawach

    f=100			#czestotliwosc probkowania
    r=rospy.Rate(f)
    k=0				#chwila poczatkowa
    kkonc=f*req.time		#chwila koncowa

    jint1=JINT()
    jint2=JINT()
    jint3=JINT()

    #path_msg = Path()###
    #path_msg.header.stamp = rospy.Time.now()###
    #path_msg.header.frame_id = 'base_link'###


    while k<=kkonc:
        joint1=jint1.interpolation(req.type, xpocz[0], req.j1,kkonc,k)
        joint2=jint2.interpolation(req.type, xpocz[1], req.j2,kkonc,k)
        gripper=jint3.interpolation(req.type, xpocz[2], req.grip,kkonc,k)
        robot.set_joints(joint1,joint2,gripper)

        state=robot.get_joint_state(f)
        pub=rospy.Publisher('joint_states',JointState,queue_size=10)
        pub.publish(state)

        path_msg=robot.get_path()###
        path_pub=rospy.Publisher('path',Path, queue_size=100)###
        path_pub.publish(path_msg)###
        #poseS=robot.get_path()###
        #path_msg.poses.append(poseS)###

        k=k+1
        r.sleep()

        #path_pub=rospy.Publisher('path',Path, queue_size=100)###
        #path_pub.publish(path_msg)###


    return jintResponse('Interpolacja zakonczona')



def jint_server():
    rospy.init_node('jint')
    s = rospy.Service('jint_control_srv', jint, handle_interpolation)
    print "Ready to interpolate."
    pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
    init_state=JointState()
    init_state.name=['base_to_link1','link1_to_link2','link2_to_link3']
    init_state.position=[0.0, 0.0, 0.0]
    init_state.velocity=[0.0, 0.0, 0.0]
    init_state.effort=[]
    init_state.header.stamp=rospy.Time.now()
    init_state.header.frame_id='base_link'
    rospy.sleep(0.5)
    pub.publish(init_state)
    ###path_pub=rospy.Publisher('/path',Path, queue_size=10)###
    
    path_msg=robot.get_path()###
    path_pub=rospy.Publisher('path',Path, queue_size=10)###
    path_pub.publish(path_msg)###
    #path_msg = Path()###
    #path_msg.header.stamp = rospy.Time.now()###
    #path_msg.header.frame_id = 'base_link'###

    #poseS=robot.get_path()###
    #path_msg.poses.append(poseS)###

    #path_pub=rospy.Publisher('path',Path, queue_size=100)###
    #path_pub.publish(path_msg)###

    #init_state = robot.get_joint_state(0)	    
    rospy.spin()


if __name__ == "__main__":
    robot = robot.Robot()
    jint_server()
