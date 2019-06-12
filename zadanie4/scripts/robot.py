import rospy
#import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
import math
from tf.transformations import *
from nav_msgs.msg import *###
import json
import os




class Robot:


    def __init__(self):
        self.joint_position=[0.0, 0.0, 0.0]
        self.previous_joint_position=[0.0, 0.0, 0.0]
        self.mainMatrix=translation_matrix( (0,0,0) )

    def set_joints(self,joint1,joint2,gripper):
        self.previous_joint_position=self.joint_position
        self.joint_position=[joint1,joint2,gripper]


    def get_joint_state(self,f):
        state = JointState()
        state.name = ['base_to_link1','link1_to_link2','link2_to_link3']
        state.position = self.joint_position
        state.velocity = [0.0, 0.0, 0.0]
        state.velocity[0] = (self.joint_position[0] - self.previous_joint_position[0])*f
        state.velocity[1] = (self.joint_position[1] - self.previous_joint_position[1])*f
        state.velocity[2] = (self.joint_position[2] - self.previous_joint_position[2])*f
        state.effort = []
        state.header.stamp = rospy.Time.now()
        state.header.frame_id = 'base_link'
        return state

    def get_path(self):
        path_msg = Path()

        poseS = PoseStamped()
        #mainMatrix = translation_matrix( (0,0,0) )
        dhparams = {}

        print os.path.dirname(os.path.realpath(__file__))
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../config/dhparams.json', 'r') as file:
            dhparams = json.loads(file.read())

        for i in range (1,3):
            a, d, alfa, theta=dhparams["i"+str(i)]
            theta=self.joint_position[i-1]
            a, d,alfa,theta= float(a),float(d),float(alfa), float(theta)
            rotx=rotation_matrix( alfa, (1,0,0) )
            transx=translation_matrix( (a,0,0) )
            rotz=rotation_matrix(theta, (0,0,1) )
            transz=translation_matrix( (0,0,d) )
            matrix= concatenate_matrices(rotx, transx, rotz, transz)
            self.mainMatrix = concatenate_matrices(self.mainMatrix,matrix)
    
        a, d, alfa, theta=dhparams["i3"]
        d=self.joint_position[2]
        a, d,alfa,theta= float(a),float(d),float(alfa), float(theta)
        rotx=rotation_matrix( alfa, (1,0,0) )
        transx=translation_matrix( (a,0,0) )
        rotz=rotation_matrix(theta, (0,0,1) )
        transz=translation_matrix( (0,0,d) )
        matrix= concatenate_matrices(rotx, transx, rotz, transz)
	    
        self.mainMatrix = concatenate_matrices(self.mainMatrix,matrix)
        x , y , z = translation_from_matrix(self.mainMatrix)
    
        poseS.header.stamp = rospy.Time.now()
        poseS.header.frame_id = "base_link"
        poseS.pose.position.x = x # x
        poseS.pose.position.y = y # y
        poseS.pose.position.z = z+d # z
    
        xq , yq , zq , wq = quaternion_from_matrix(self.mainMatrix)	    
        poseS.pose.orientation.x = xq
        poseS.pose.orientation.y = yq
        poseS.pose.orientation.z = zq
        poseS.pose.orientation.w = wq


        path_msg.header.stamp = rospy.Time.now()
        path_msg.header.frame_id = 'base_link'
        path_msg.poses.append(poseS)

        return path_msg

        #return poseS
