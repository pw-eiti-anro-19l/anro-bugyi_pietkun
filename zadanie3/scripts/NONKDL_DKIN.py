import rospy
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import Marker

pub = rospy.Publisher('poseStamped', PoseStamped , queue_size=100)
marker_pub = rospy.Publisher('visualization', Marker, queue_size=100)

dhparam = {}
with open('../source/dhparams.json','r') as file:
dhparams = json.loads(file.read())


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    poseS = PoseStamped()
    mainMatrix = translation_matrix( (0,0,0) )
    for i range (0,2):
	    theta = data.position[i]
	    rotx=rotation_matrix( alfa, (1,0,0) )
	    transx=translation_matrix( (a,0,0) )
	    rotz=rotation_matrix(theta, (0,0,1) )
	    transz=translation_matrix( (0,0,0) )
	    matrix= concatenate_matrices(transz, rotz, rotx, transx)
	    
	    mainMatrix = concatenate_matrices(mainMatrix,matrix)
    
    d = data.position[2]
    rotx=rotation_matrix( alfa, (1,0,0) )
    transx=translation_matrix( (a,0,0) )
    rotz=rotation_matrix(0, (0,0,1) )
    transz=translation_matrix( (0,0,d) )
    matrix= concatenate_matrices(transz, rotz, rotx, transx)
	    
    mainMatrix = concatenate_matrices(mainMatrix,matrix)
    x , y , z = translation_from_matrix(mainMatrix)
    
    poseS.header.stamp = rospy.Time.now()
    poseS.header.frame_id = "map"
    poseS.pose.position.x = x
    poseS.pose.position.y = y
    poseS.pose.position.z = z
    	

    
    xq , yq , zq , wq = quaternion_from_matrix(mainMatrix)	    
    poseS.pose.orientation.x = xq
    poseS.pose.orientation.y = yq
    poseS.pose.orientation.z = zq
    poseS.pose.orientation.w = wq

	pub.publish(poseS)
	
	marker = Marker()
	marker.header.frame_id = "point";
	marker.header.stamp = ros::Time();
	marker.ns = "my_namespace";
	marker.id = 0;
	marker.type = visualization_msgs::Marker::SPHERE;
	marker.action = visualization_msgs::Marker::ADD;
	marker.pose.position.x = x;
	marker.pose.position.y = y;
	marker.pose.position.z = z;
	marker.pose.orientation.x = xq;
	marker.pose.orientation.y = yq;
	marker.pose.orientation.z = zq;
	marker.pose.orientation.w = wq;
	marker.scale.x = 0.1;
	marker.scale.y = 0.1;
	marker.scale.z = 0.1;
	marker.color.a = 1.0; // Don't forget to set the alpha!
	marker.color.r = 1;
	marker.color.g = 0;
	marker.color.b = 1;

	marker_pub.publish( marker );
	

def listener():


    rospy.init_node('NONKDL_DKIN', anonymous=True)

    rospy.Subscriber("joint_states", JointState , callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    try:
	listener()        
    except rospy.ROSInterruptException:
        pass


    
