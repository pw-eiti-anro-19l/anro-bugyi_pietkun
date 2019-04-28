#! /usr/bin/python
import rospy
import json
import os
from PyKDL import *
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import Marker
from tf.transformations import *

pub = rospy.Publisher('poseStamped', PoseStamped , queue_size = 100 )

dhparams = {}
#with open('../config/dhparams.json', 'r') as file:
    #dhparams = json.loads(file.read())

print os.path.dirname(os.path.realpath(__file__))
with open(os.path.dirname(os.path.realpath(__file__)) + '/../config/dhparams.json', 'r') as file:
    dhparams = json.loads(file.read())

def newFrame(a, d, alfa, theta)
    rotx=rotation_matrix( alfa, (1,0,0) )
    transx=translation_matrix( (a,0,0) )
    rotz=rotation_matrix(theta, (0,0,1) )
    transz=translation_matrix( (0,0,d)
    matrix= concatenate_matrices(rotx, transx, rotz, transz)
	return Vector(translation_from_matrix(matrix))

def callback(data):
    poseS = PoseStamped()
    mainMatrix = translation_matrix( (0,0,0) )
    robot = PyKDL.Chain()

   for i in range (1,3):
        a, d, alfa, theta=dhparams["i"+str(i)]
	    a, d,alfa,theta= float(a),float(d),float(alfa), float(theta)
	    
		joint = Joint(Joint.RotZ)
		frame = Frame ( newFrame(a,d,alfa,data.position[-1]))
		segment = Segment(joint, frame)
		robot.addSegment(segment)
	
    a, d, alfa, theta=dhparams["i"+str(i)]
	a, d,alfa,theta= float(a),float(d),float(alfa), float(theta)
    joint = Joint(Joint.RotZ)
	frame = Frame ( newFrame(a,data.position[2],alfa,theta)
	segment2 = Segment(joint, frame)
	robot.addSegment( segment2 )
	    
    wynik = frame2
    
	poseS.header.stamp = rospy.Time.now()
    poseS.header.frame_id = "base_link"
    poseS.pose.position.x = wynik.p.x()
    poseS.pose.position.y = wynik.p.y()
    poseS.pose.position.z = wynik.p.z()
    
	xq , yq , zq , wq = wynik.M.GetQuaternion()	    
    poseS.pose.orientation.x = xq
    poseS.pose.orientation.y = yq
    poseS.pose.orientation.z = zq
    poseS.pose.orientation.w = wq

    pub.publish(poseS)
	
	

def listener():


    rospy.init_node('NONKDL', anonymous=True)

    rospy.Subscriber("joint_states", JointState , callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    try:
	listener()        
    except rospy.ROSInterruptException:
        pass

