from params import *
import numpy as np
import eqs
from show import show

	

def run(T, playback_speedup=0.1, tau=0.001):
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

	show('no_control.html',bot.state_log,tau/playback_speedup)


class Robot():
	def __init__(self,x=0.3, y=0., a=1.6, b=1.15):
		self.q = np.array([x,y,a,b])
		self.q_d = np.zeros(4)
		self.psi = 0.715
		self.state_log = []

	def next_pos(self,tau):
		if self.q[1] > 0: # flies
			self.q_d = self.next_flying_pos(tau)
		else: # stands
			self.q_d = self.next_standing_pos(tau)	
			
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
		
		q_d = self.q_d + np.hstack([np.zeros(2),tau * np.linalg.inv(C).dot(D)])
		return q_d
	

	def next_flying_pos(self,tau):
		C = np.vstack([
			x_f.get_c1(self.q,self.q_d,self.psi),
			y_f.get_c2(self.q,self.q_d,self.psi),
			a_f.get_c3(self.q,self.q_d,self.psi),
			b_f.get_c4(self.q,self.q_d,self.psi)
			])
		D = - np.array([
			x_f.get_d1(self.q, self.q_d,self.psi),
			y_f.get_d2(self.q,self.q_d,self.psi),
			a_f.get_d3(self.q,self.q_d,self.psi),
			b_f.get_d4(self.q,self.q_d,self.psi)
			])
		return self.q_d + np.hstack([tau * np.linalg.inv(C).dot(D), np.zeros(1)])
		

	def fell(self):
		_,_,a,b = self.q
		return b < 0 or L2*np.sin(b) + 2*L1*np.sin(a+b) < 0




