from params import *
import numpy as np
import eqs, eqf
from show import show
import reinforce
from reinforce import reward_balance, reward_hop, reward_salto


def run(T, speedup=0.1, tau=0.001):
	assert tau < 0.1
	assert tau > 0
	assert T > 0

	bot = Robot()
	bot.init_randomly_standing()
	t = 0
	while t < T:
		bot.psi = get_psi(get_policy(bot.q,bot.q_d))
		bot.next_pos(tau)
		t += tau
		if bot.fell(): break

	show('no_control.html',bot.pos_log,tau/speedup)


class Robot():
	def __init__(self,x=0.3, y=0., a=2.2, b=1.0):
		self.q = np.array([x,y,a,b])
		self.q_d = np.zeros(4)
		self.psi = 0.6
		self.Q = {'balance':{}, 'hop':{}, 'salto':{}}
		self.reward_func = {'balance':'reward_balance', 
							'hop':'reward_hop',
							'salto':'reward_salto'}
		self.pos_log = []

	def init_randomly_standing(self):
		self.q = np.array([0.4, 0., np.random.uniform(0.1, 3.),np.random.uniform(0.1,1.8)])
		self.q_d = np.zeros(4)


	def correct_state(self,tau):
		#self.q[1] = 0.
		x,y,a,b = self.q
		
		A = np.array([
			[-L1*np.sin(a+b),  -L2*np.sin(b)-L1*np.sin(a+b)],
			[ L1*np.cos(a+b),   L2*np.cos(b)+L1*np.cos(b)]
			])
		da,db = np.linalg.inv(A).dot(np.array([self.q_d[0],self.q_d[1]]))
		self.q_d = np.array([0., 0., self.q_d[2]+da, self.q_d[3]+db])
		


	def next_pos(self,tau):
		if self.q[1] > 0.: # flies
			self.q_d = self.next_flying_pos(tau)
			#print 'flying:',self.q, self.q_d
			self.q += tau * self.q_d
			if self.q[1] < 0: self.correct_state(tau)
				
		else: # stands
			qd_s = self.next_standing_pos(tau)
			qd_f = self.next_flying_pos(tau)
			#print 'standing:', self.q, self.q_d
				
			if qd_f[1] > 0.: self.q_d = qd_f
			else: self.q_d = qd_s
			
			self.q += tau * self.q_d

		

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
		_,y,a,b = self.q
		return y + L2*np.sin(b) < 0 or \
			   y + L2*np.sin(b) + 2*L1*np.sin(a+b) < 0



	def train(self, episode_len, episode_nbr, behavior='balance'):
		tau = 0.001
		speedup = 0.1
		self.pos_log = []
		for j in range(episode_nbr):			
			self.run_episode(episode_len,tau,behavior,'train')
			if (j+1)%10 == 0: print "%i episodes run" % (j+1)
	
		self.run_episode(episode_len,tau,behavior,'show')
		
		show(behavior+'.html',self.pos_log,tau/speedup)


	def run_episode(self, episode_len, tau, behavior, mode):
		t = 0
		reward = getattr(reinforce, self.reward_func[behavior])
		if mode == 'train': self.init_randomly_standing()
		elif mode == 'show': 
			self.q = np.array([0.4, 0., 1.5, 1.1])
			self.q_d = np.zeros(4)

		state = reinforce.get_state(self.q,self.q_d)
		action = reinforce.get_policy(state,self.Q[behavior])
		psi = reinforce.get_psi(action)
		i = 0
		while t < episode_len:
			t += tau
			i += 1
			if i%10 == 0: 
				next_state = reinforce.get_state(self.q,self.q_d)
				rwd = reward(state,action,next_state,self.Q[behavior])
				if mode == 'train': reinforce.learn(self.Q[behavior],state,action,next_state,rwd)
				
				action = reinforce.get_policy(next_state,self.Q[behavior])
				state = next_state
				psi = reinforce.get_psi(action)

			if mode == 'show': self.pos_log.append(tuple(self.q))
			
			self.next_pos(tau)
			self.psi = psi # latency for one step added intentionally 

			if self.fell(): break




