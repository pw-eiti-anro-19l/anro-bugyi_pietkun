#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
import json
import os
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
from math import *
from tf.transformations import *

pub = rospy.Publisher('joint_states', JointState, queue_size = 100 )


dhparams = {}
#with open('../config/dhparams.json', 'r') as file:
    #dhparams = json.loads(file.read())

print os.path.dirname(os.path.realpath(__file__))
with open(os.path.dirname(os.path.realpath(__file__)) + '/../config/dhparams.json', 'r') as file:
    dhparams = json.loads(file.read())

pkat2=0
pkat1=0
def callback(data):
	global pkat1
	global pkat2	
	js=JointState()
	px=data.pose.position.x
	py=data.pose.position.y
	pz=data.pose.position.z
	if px == 0 and py == 0:
		px=0.1
		py=0.1
	a1,d,e,f=dhparams["i2"]
	a2,d,e,f=dhparams["i3"]
	przesuw3=0.3-pz
		
	kat2v2=-acos((px**2+py**2-a1**2-a2**2)/(2*a1*a2))
	kat1v2=asin((a2*sin(kat2v2))/(sqrt(px**2+py**2)))+atan2(py,px)
	
	kat2v1=acos((px**2+py**2-a1**2-a2**2)/(2*a1*a2))
	kat1v1=-asin((a2*sin(kat2v1))/(sqrt(px**2+py**2)))+atan2(py,px)
	if fabs(pkat1-kat1v1)>fabs(pkat1-kat1v2) :
		pkat1=kat1v2
		pkat2=kat2v2
	else :
		pkat1=kat1v1
		pkat2=kat2v1	
	js.header = Header()
	js.header.stamp = rospy.Time.now()
	js.name = ['base_to_link1','link1_to_link2','link2_to_link3']
	js.position= [ pkat1 , pkat2 , przesuw3 ]
	js.velocity= []
	js.effort= []
	pub.publish(js)
	

	

def listener():


    rospy.init_node('IKIN', anonymous=True)

    rospy.Subscriber("/pose_stamped", PoseStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    try:
	listener()        
    except rospy.ROSInterruptException:
        pass
