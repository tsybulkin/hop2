import numpy as np
from numpy import sin, cos
from params import *


def get_c1(q, q_d, psi=0):
	x,y,a,b = q
	x_d,y_d,a_d,b_d = q_d

	return np.array([
		I+ L1**2*m, 
		L1**2*m + L1*L2*m*cos(a)
		]) 

def get_d1(q, q_d, psi=0):
	x,y,a,b,g = q
	x_d,y_d,a_d,b_d,_ = q_d
	return G*L1*m*cos(a + b) \
		+ L1*L2*m*sin(a)*b_d**2 \
		+ dz*k1*z1*sin(a) - dz*k2*z2*sin(a) \
		+ k1*z0*z1*sin(psi)*sin(a) - k1*z1**2*sin(a)*cos(a) \
		+ k2*z0*z2*sin(psi)*sin(a) - k2*z2**2*sin(a)*cos(a) \
		+ miu_a*a_d