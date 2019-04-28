#! /usr/bin/python
import rospy
import json
import os
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import Marker
from tf.transformations import *

pub = rospy.Publisher('poseStamped', PoseStamped , queue_size = 100 )

marker_pub = rospy.Publisher('visualization_marker', Marker , queue_size = 100 )

dhparams = {}
#with open('../config/dhparams.json', 'r') as file:
    #dhparams = json.loads(file.read())

print os.path.dirname(os.path.realpath(__file__))
with open(os.path.dirname(os.path.realpath(__file__)) + '/../config/dhparams.json', 'r') as file:
    dhparams = json.loads(file.read())

def callback(data):
    poseS = PoseStamped()
    mainMatrix = translation_matrix( (0,0,0) )
    for i in range (1,3):
        a, d, alfa, theta=dhparams["i"+str(i)]
	a, d,alfa,theta= float(a),float(d),float(alfa), float(theta)
	rotx=rotation_matrix( alfa, (1,0,0) )
	transx=translation_matrix( (a,0,0) )
	rotz=rotation_matrix(data.position[i-1], (0,0,1) )
	transz=translation_matrix( (0,0,d) )
        matrix= concatenate_matrices(rotx, transx, rotz, transz)
        mainMatrix = concatenate_matrices(mainMatrix,matrix)
    
    a, d, alfa, theta=dhparams["i3"]
    a, d,alfa,theta= float(a),float(d),float(alfa), float(theta)
    rotx=rotation_matrix( alfa, (1,0,0) )
    transx=translation_matrix( (a,0,0) )
    rotz=rotation_matrix(theta, (0,0,1) )
    transz=translation_matrix( (0,0,data.position[2]) )
    matrix= concatenate_matrices(rotx, transx, rotz, transz)
	    
    mainMatrix = concatenate_matrices(mainMatrix,matrix)
    x , y , z = translation_from_matrix(mainMatrix)
    
    poseS.header.stamp = rospy.Time.now()
    poseS.header.frame_id = "base_link"
    poseS.pose.position.x = x # x
    poseS.pose.position.y = y # y
    poseS.pose.position.z = z # z
    	

    
    xq , yq , zq , wq = quaternion_from_matrix(mainMatrix)	    
    poseS.pose.orientation.x = xq
    poseS.pose.orientation.y = yq
    poseS.pose.orientation.z = zq
    poseS.pose.orientation.w = wq

    pub.publish(poseS)
	
    marker = Marker()
    marker.header.frame_id = "base_link" # link3
    marker.header.stamp = rospy.Time.now()
    marker.ns = "robot"
    marker.id = 0
    marker.type = 2 # sphere
    marker.action = 0 # add
    marker.pose.position.x = x # x
    marker.pose.position.y = y # y
    marker.pose.position.z = z+d # z
    marker.pose.orientation.x = xq
    marker.pose.orientation.y = yq
    marker.pose.orientation.z = zq
    marker.pose.orientation.w = wq
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1
    marker.color.a = 1.0 
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 1.0
    marker.lifetime = rospy.Duration(0)
    marker_pub.publish( marker )
	

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


    
