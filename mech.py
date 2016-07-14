from sympy import cos, sin, diff, symbols
from sympy.physics.mechanics import LagrangesMethod, dynamicsymbols


def init_standing(): return dynamicsymbols('a b gama')

def Ls(a,b,gama):
	g,m1,m2,L1,L2,L3,I1,I2,eps,x,y,z0,z1,z2,z3,k1,k2,k3,dz,da,psi = \
	symbols('g m1 m2 L1 L2 L3 I1 I2 eps x y z0 z1 z2 z3 k1 k2 k3 dz da psi')

	a_d, b_d, gama_d = dynamicsymbols('a b gama',1)

	x1 = x + L3*cos(b) + L2*cos(b+gama) + L1*cos(a+b+gama)
	y1 = y + L3*sin(b) + L2*sin(b+gama) + L1*cos(a+b+gama)

	x2 = x + L3*cos(b) + L2*eps*cos(b+gama)
	y2 = y + L3*sin(b) + L2*eps*sin(b+gama)

	u1 = dz + z0*sin(psi) - z1*cos(a)
	u2 = dz - z0*sin(psi) + z2*cos(a)
	u3 = da - z3*cos(gama)

	T = m1/2*(x1.diff('t')**2 + y1.diff('t')**2) + I1/2*(a_d**2 + b_d**2 + gama_d**2) + \
		m2/2*(x2.diff('t')**2 + y2.diff('t')**2) + I2/2*(b_d + gama_d)**2

	V = m1*g*y1 + k1/2*u1**2 + k2/2*u2**2 + m2*g*y2 + k3/2*u3**2

	return T-V


def init_flying(): return dynamicsymbols('x y a b')


def Lf(x,y,a,b):
	Grav,m1,m2,L1,L2,L3,I1,I2,eps,g0,z0,z1,z2,z3,k1,k2,k3,dz,da,psi = \
	symbols('Grav m1 m2 L1 L2 L3 I1 I2 eps g0 z0 z1 z2 z3 k1 k2 k3 dz da psi')

	x_d, y_d, a_d, b_d = dynamicsymbols('x y a b',1)

	x1 = x + L3*cos(b) + L2*cos(b+g0) + L1*cos(a+b+g0)
	y1 = y + L3*sin(b) + L2*sin(b+g0) + L1*cos(a+b+g0)

	x2 = x + L3*cos(b) + L2*eps*cos(b+g0)
	y2 = y + L3*sin(b) + L2*eps*sin(b+g0)

	u1 = dz + z0*sin(psi) - z1*cos(a)
	u2 = dz - z0*sin(psi) + z2*cos(a)
	
	T = m1/2*(x1.diff('t')**2 + y1.diff('t')**2) + I1/2*(a_d**2 + b_d**2) + \
		m2/2*(x2.diff('t')**2 + y2.diff('t')**2) + I2/2*(b_d)**2

	V = m1*Grav*y1 + m2*Grav*y2 + k1/2*u1**2 + k2/2*u2**2 

	return T-V

