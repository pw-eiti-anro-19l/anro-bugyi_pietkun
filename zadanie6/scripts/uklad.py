import rospy
#import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from tf.transformations import quaternion_from_euler
import math
from tf.transformations import *
from nav_msgs.msg import *###
import json
import os




class Uklad:


    def __init__(self):
        self.pos=[0.0, 0.0, 0.0]
        self.orient=[0.0, 0.0, 0.0, 0.0]


    def set_coordinates(self,x_val,y_val,z_val,roll_val,pitch_val,yaw_val):
        self.pos=[x_val,y_val,z_val]
        self.orient=[roll_val,pitch_val,yaw_val]


    def get_pose(self):
        state = PoseStamped()

        state=PoseStamped()
        state.header.stamp = rospy.Time.now()
        state.header.frame_id = 'base_link'
        state.pose.position.x=self.pos[0]
        state.pose.position.y=self.pos[1]
        state.pose.position.z=self.pos[2]


        quat = quaternion_from_euler(self.orient[0],self.orient[1],self.orient[2])
        state.pose.orientation.x = quat[0]
        state.pose.orientation.y = quat[1]
        state.pose.orientation.z = quat[2]
        state.pose.orientation.w = quat[3]

        return state

