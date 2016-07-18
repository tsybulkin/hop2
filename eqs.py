import numpy as np
from params import *


def get_c1(q, q_d, psi=0):
	x,y,a,b = q
	x_d,y_d,a_d,b_d = q_d

	return np.array([
		I1 + L1**2*m1, 
		I1 + L1**2*m1 + L1*L2*m1*np.cos(a)
		]) 

def get_d1(q, q_d, psi=0):
	x,y,a,b = q
	x_d,y_d,a_d,b_d = q_d
	return G*L1*m1*np.cos(a + b) \
		+ L1*L2*m1*np.sin(a)*b_d**2 \
		+ dz*k1*z1*np.sin(a) - dz*k2*z2*np.sin(a) \
		+ k1*z0*z1*np.sin(psi)*np.sin(a) - k1*z1**2*np.sin(a)*np.cos(a) \
		+ k2*z0*z2*np.sin(psi)*np.sin(a) - k2*z2**2*np.sin(a)*np.cos(a) \
		+ miu_a*a_d


def get_c2(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d

	return np.array([
		I1 + L1**2*m1 + L1**2*m1 + L1*L2*m1*np.cos(a),
		I1 + I2 + (L1**2+L2**2)*m1 + 2*L1*L2*m1*np.cos(a) + L2**2*m2/4
		])
		
def get_d2(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d
	return G*L1*m1*np.cos(a + b) + G*L2*m1*np.cos(b) + G*L2*m2*np.cos(b)/2 \
		- L1*L2*m1*np.sin(a)*a_d**2 - 2*L1*L2*m1*np.sin(a)*a_d*b_d 

