import numpy as np
from numpy import sin, cos
from params import *


def get_c1(q, q_d, psi=0):
	x,y,a,b = q
	x_d,y_d,a_d,b_d = q_d

	return np.array([
		m1 + m2,
		0,
		-L1*m1*sin(a + b), 
		-L1*m1*sin(a + b) - L2*m1*sin(b) - L2*m2*sin(b)/2 
		]) 

def get_d1(q, q_d, psi=0):
	x,y,a,b = q
	x_d,y_d,a_d,b_d = q_d
	return - L1*m1*cos(a + b)*(a_d**2 + b_d**2) \
		- 2*L1*m1*cos(a + b)*a_d*b_d - L2*m1*cos(b)*b_d**2 - L2/2*m2*cos(b)*b_d**2 



def get_c2(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d

	return np.array([
		0,
		m1 + m2,
		L1*m1*cos(a + b),
		L1*m1*cos(a + b) + L2*m1*cos(b) + L2*m2*cos(b)/2 
		])
		

def get_d2(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d
	return G*m1 + G*m2 \
		- L1*m1*sin(a + b)*a_d**2 \
		- 2*L1*m1*sin(a + b)*a_d*b_d \
		- L1*m1*sin(a + b)*b_d**2 \
		- L2*m1*sin(b)*b_d**2 \
		- L2*m2*sin(b)*b_d**2/2 



def get_c3(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d

	return np.array([
		-L1*m1*sin(a + b),
		L1*m1*cos(a + b),
		I1 + (L1**2)*m1,
		I1 + L1*L2*m1*cos(a)+ L1**2*m1
		])

def get_d3(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d
	return G*L1*m1*cos(a + b) \
		+ L1*L2*m1*sin(a)*b_d**2 \
		+ dz*k1*z1*sin(a) - dz*k2*z2*sin(a) \
		+ k1*z0*z1*sin(psi)*sin(a) - k1*z1**2*sin(a)*cos(a) \
		+ k2*z0*z2*sin(psi)*sin(a) - k2*z2**2*sin(a)*cos(a) \
		+ miu_a*a_d



def get_c4(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d

	return np.array([
		- L1*m1*sin(a + b) - L2*m1*sin(b) - L2*m2*sin(b)/2, 
		+ L1*m1*cos(a + b) + L2*m1*cos(b) + L2*m2*cos(b)/2,	
		I1 + (L1**2)*m1 + L1*L2*m1*cos(a),
		I1 + I2 + L1**2*m1 + 2*L1*L2*m1*cos(a) + L2**2*m1 + L2**2*m2/4 
		])

def get_d4(q, q_d, psi=0):
	_,_,a,b = q
	_,_,a_d,b_d = q_d
	return G*L1*m1*cos(a + b) + G*L2*m1*cos(b) + G*L2*m2*cos(b)/2 \
		- L1*L2*m1*sin(a)*a_d**2 - 2*L1*L2*m1*sin(a)*a_d*b_d 


