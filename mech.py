from sympy import cos, sin, diff, symbols
from sympy.physics.mechanics import LagrangesMethod, dynamicsymbols


def init_standing(): return dynamicsymbols('a b')

def Ls(a,b):
	G,m1,m2,L1,L2,I1,I2,x,y,z0,z1,z2,k1,k2,dz,psi = \
	symbols('G m1 m2 L1 L2 I1 I2 x y z0 z1 z2 k1 k2 dz psi')

	a_d, b_d = dynamicsymbols('a b',1)

	x1 = x + L2*cos(b) + L1*cos(a+b)
	y1 = y + L2*sin(b) + L1*sin(a+b)

	x2 = x + L2*cos(b)/2
	y2 = y + L2*sin(b)/2

	u1 = dz + z0*sin(psi) - z1*cos(a)
	u2 = dz - z0*sin(psi) + z2*cos(a)
	
	T = m1/2*(x1.diff('t')**2 + y1.diff('t')**2) + I1/2*(a_d + b_d)**2 \
		+ m2/2*(x2.diff('t')**2 + y2.diff('t')**2) + I2/2*b_d**2
	V = m1*G*y1 + m2*G*y2 + k1/2*u1**2 + k2/2*u2**2 

	return T-V


def init_flying(): return dynamicsymbols('x y a b')


def Lf(x,y,a,b):
	G,m1,m2,L1,L2,I1,I2,z0,z1,z2,k1,k2,dz,psi = \
	symbols('G m1 m2 L1 L2 I1 I2 z0 z1 z2 k1 k2 dz psi')

	x_d, y_d, a_d, b_d = dynamicsymbols('x y a b',1)

	x1 = x + L2*cos(b) + L1*cos(a+b)
	y1 = y + L2*sin(b) + L1*sin(a+b)

	x2 = x + L2*cos(b)/2
	y2 = y + L2*sin(b)/2

	u1 = dz + z0*sin(psi) - z1*cos(a)
	u2 = dz - z0*sin(psi) + z2*cos(a)
	
	T = m1/2*(x1.diff('t')**2 + y1.diff('t')**2) + I1/2*(a_d + b_d)**2 \
		+ m2/2*(x2.diff('t')**2 + y2.diff('t')**2) + I2/2*b_d**2
	V = m1*G*y1 + m2*G*y2 + k1/2*u1**2 + k2/2*u2**2 

	return T-V

