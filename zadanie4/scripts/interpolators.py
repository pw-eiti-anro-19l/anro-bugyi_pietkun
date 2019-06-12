import numpy as np
class JINT:

    def __init__(self):
        self.last_t=1000
        self.last_params=np.matrix('0;0;0;0;0;0')

    def linear(self,x0,x1,time,t):
        a=(x1-x0)/(time)
        return x0+a*t

    def trapezoid(self, x0, x1, time, t):
        if self.last_t == (t - 1):
            params = self.last_params
        else:
            spline_array = np.array([[0, 0, 1, 0, 0, 0, 0, 0],
				  [0, 0, 0, 0, 0, time**2, time, 1],
				  [(time**2)/25, time/5, 1, -time/5, -1, 0, 0, 0],
				  [0, 0, 0, 4*time/5, 1, -(4*time/5)**2, -4*(time/5), -1],
				  [2*time/5, 1, 0, -1, 0, 0, 0, 0],
				  [0, 0, 0, 1, 0, -8*time/5, -1, 0],
				  [0, 1, 0, 0, 0, 0, 0, 0],
				  [0, 0, 0, 0, 0, 2*time, 1, 0]])
            b = np.array([[x0],[x1],[0],[0],[0],[0],[0],[0]])
            params = np.linalg.solve(spline_array, b)
            params = params.tolist()
            self.last_params = params
			
        self.last_t = t

        if t < (time/5):
            return params[0][0]*(t**2) + params[1][0]*t + params[2][0]
        if t >= time/5 and t < (4*time/5):
            return params[3][0]*t + params[4][0]
        else:
            return params[5][0]*(t**2) + params[6][0]*t + params[7][0]


    def interpolation(self,type,x0,x1,time,t):
        if type == 'linear':
            return self.linear(x0,x1,time,t)
        if type == 'trapezoid':
            return self.trapezoid(x0,x1,time,t)
