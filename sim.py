from params import *
import numpy as np
import eqs, eqf
from show import show

	

def run(T, speedup=0.1, tau=0.001):
	assert tau < 0.1
	assert tau > 0
	assert T > 0
	
	bot = Robot()
	t = 0
	while t < T:
		bot.next_pos(tau)
		t += tau
		#print '\nt =', t, 'pos:\n', bot.q, bot.q_d
		if bot.fell(): break

	show('no_control.html',bot.state_log,tau/speedup)


class Robot():
	def __init__(self,x=0.8, y=0., a=2.35, b=1.25):
		self.q = np.array([x,y,a,b])
		self.q_d = np.zeros(4)
		self.psi = 0.8
		self.state_log = []

	def correct_state(self,tau):
		self.q[1] = 0.
		x,y,a,b = self.q
		
		A = np.array([
			[-L1*np.sin(a+b),  -L2*np.sin(b)-L1*np.sin(a+b)],
			[ L1*np.cos(a+b),   L2*np.cos(b)+L1*np.cos(b)]
			])
		da,db = np.linalg.inv(A).dot(np.array([self.q_d[0],self.q_d[1]]))
		self.q_d = np.array([0., 0., self.q_d[2]+da, self.q_d[3]+db])
		"""
		x1 = x + L2*np.cos(b) + L1*np.cos(a+b)
		y1 = y + L2*np.sin(b) + L1*np.sin(a+b)
		new_db = np.cross(np.array([np.cos(b),np.sin(b)]),np.array([self.q_d[0],self.q_d[1]]))/L2
		new_da = np.cross(np.array([np.cos(a+b),np.sin(a+b)]),np.array([self.q_d[0],self.q_d[1]]))/L1
		self.q_d = np.array([0., 0., new_da, 0])
		"""
		


	def next_pos(self,tau):
		if self.q[1] > 0.: # flies
			self.q_d = self.next_flying_pos(tau)
			print 'flying:',self.q, self.q_d
			self.q += tau * self.q_d
			if self.q[1] < 0: self.correct_state(tau)
				
		else: # stands
			qd_s = self.next_standing_pos(tau)
			qd_f = self.next_flying_pos(tau)
			print 'standing:', self.q, self.q_d
				
			if qd_f[1] > 0.: self.q_d = qd_f
			else: self.q_d = qd_s
			
			self.q += tau * self.q_d

		self.state_log.append(tuple(self.q))


	def next_standing_pos(self,tau):
		C = np.array([
			eqs.get_c1(self.q,self.q_d,self.psi),
			eqs.get_c2(self.q,self.q_d,self.psi),
			])
		D = - np.array([
			eqs.get_d1(self.q, self.q_d,self.psi),
			eqs.get_d2(self.q,self.q_d,self.psi),
			])
		
		return self.q_d + np.hstack([np.zeros(2),tau * np.linalg.inv(C).dot(D)])
		

	def next_flying_pos(self,tau):
		C = np.vstack([
			eqf.get_c1(self.q,self.q_d,self.psi),
			eqf.get_c2(self.q,self.q_d,self.psi),
			eqf.get_c3(self.q,self.q_d,self.psi),
			eqf.get_c4(self.q,self.q_d,self.psi)
			])
		D = - np.array([
			eqf.get_d1(self.q, self.q_d,self.psi),
			eqf.get_d2(self.q,self.q_d,self.psi),
			eqf.get_d3(self.q,self.q_d,self.psi),
			eqf.get_d4(self.q,self.q_d,self.psi)
			])
		
		return self.q_d + tau * np.linalg.inv(C).dot(D)
		

	def fell(self):
		_,_,a,b = self.q
		return b < 0 or L2*np.sin(b) + 2*L1*np.sin(a+b) < 0




