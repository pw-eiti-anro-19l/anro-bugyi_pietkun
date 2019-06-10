#!/usr/bin/env python

import rospy
from tf import TransformListener
from sensor_msgs.msg import JointState
import json
import os
from math import *
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
from math import *
from tf import *
import time
import tf
from tf.transformations import *

pub = rospy.Publisher('nasz_blad', PoseStamped, queue_size = 100 )

listener1 = 0
dhparams = {}
#with open('../config/dhparams.json', 'r') as file:
    #dhparams = json.loads(file.read())
trans=[0,0,0]
print os.path.dirname(os.path.realpath(__file__))
with open(os.path.dirname(os.path.realpath(__file__)) + '/../config/dhparams.json', 'r') as file:
    dhparams = json.loads(file.read())

pkat2=0
pkat1=0
def callback(data):
    global listener1
    rate = rospy.Rate(10.0)
    global trans
    print(trans)
    (trans,rot) = listener1.lookupTransform('/base_link', '/link3', rospy.Time(0))
    nerror=PoseStamped()
    nerror=data
    print(trans)
    nerror.pose.position.x=fabs(data.pose.position.x-trans[0])
    nerror.pose.position.y=fabs(data.pose.position.y-trans[1])
    nerror.pose.position.z=fabs(data.pose.position.z-trans[2])
    #nerror.pose.position.x=trans[0]
    #nerror.pose.position.y=trans[1]
    #nerror.pose.position.z=trans[2]
    pub.publish(nerror)
	#nerror=PoseStamped()
	#nerror=data
	#nerror.pose.position.x=data.pose.position.x-trans[0]
        #nerror.pose.position.y=data.pose.position.y-trans[1]
        #nerror.pose.position.z=data.pose.position.z-trans[2]
	#pub.publish(nerror)
   
	

def listener():

    rospy.init_node('IKINerror', anonymous=True)
    global listener1
    listener1 = tf.TransformListener()
    rospy.Subscriber("pose_stamped", PoseStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    try:
	listener()        
    except rospy.ROSInterruptException:
        pass