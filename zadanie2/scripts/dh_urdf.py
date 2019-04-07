import json
from tf.transformations import *



dhparam = {}
with open('../source/dhparams.json','r') as file:
	dhparams = json.loads(file.read())
a,b,c,d=dhparams["i2"]
with open('../config/urdf.yaml','w') as file:
	for i in range(1,int(dhparams["number"])+1) :
		a,d,alfa,theta=dhparams["i"+str(i)]

		
		
		rotx=rotation_matrix( alfa, (1,0,0) )
		transx=translation_matrix( (a,0,0) )
		rotz=rotation_matrix(theta, (0,0,1) )
		transz=translation_matrix( (0,0,d) )

		matrix= concatenate_matrices(transz, rotz, rotx, transx)
		
		rpy = euler_from_matrix(matrix)
		xyz=translation_from_matrix(matrix)
		
		file.write("i"+str(i) + ":\n")
		file.write(" rpy: {} {} {}\n".format(*xyz))
		file.write(" xyz: {} {} {}\n".format(*rpy))
		file.write(" length: {}\n".format(a))
		file.write("\n")


