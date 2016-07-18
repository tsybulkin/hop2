from params import *
import numpy as np
import eqs, eqf
from show import show
import reinforce
from reinforce import reward_balance, reward_hop, reward_salto

EPS = 0.2

def run(T, speedup=0.1, tau=0.001):
	assert tau < 0.1
	assert tau > 0
	assert T > 0

	bot = Robot()
	bot.q = np.array([0.3, 0., 2.8, 1.2])
	bot.psi = 1.
	t = 0
	while t < T:
		#bot.psi = get_psi(get_policy(EPS,bot.q,bot.q_d))
		bot.next_pos(tau)
		t += tau
		bot.pos_log.append(tuple(bot.q))
		if bot.is_down(): break

	show('no_control.html',bot.pos_log,tau/speedup)


class Robot():
	def __init__(self,x=0.3, y=0., a=2.2, b=1.2):
		self.q = np.array([x,y,a,b])
		self.q_d = np.zeros(4)
		self.psi = 0.3
		self.Q = {'balance':{}, 'hop':{}, 'salto':{}}
		self.reward_func = {'balance':'reward_balance', 
							'hop':'reward_hop',
							'salto':'reward_salto'}
		self.pos_log = []

	def init_randomly_standing(self):
		self.psi = 0.
		self.q = np.array([0.4, 0., np.random.uniform(0.5, 1.8),np.random.uniform(0.5,1.8)])
		self.q_d = np.zeros(4)


	def correct_state(self):
		#self.q[1] = 0.
		x,y,a,b = self.q
		
		A = np.array([
			[-L1*np.sin(a+b),  -L2*np.sin(b)-L1*np.sin(a+b)],
			[ L1*np.cos(a+b),   L2*np.cos(b)+L1*np.cos(b)]
			])
		try:
			A1 = np.linalg.inv(A)
		except:
			self.q_d = np.array([0., 0., self.q_d[2]+0, self.q_d[3]+0])
		else:
			da,db = A1.dot(np.array([self.q_d[0],self.q_d[1]]))	
			self.q_d = np.array([0., 0., self.q_d[2]+da, self.q_d[3]+db])

	def correct_state1(self):
		x,y,a,b = self.q
		dx,dy,da,db = self.q_d
		print 'velosities:',self.q_d
		v2 = db*np.array([dx-L2*np.sin(b), dy+L2*np.cos(b)])
		v1 = v2 + L1+(da+db)*np.array([-np.sin(a+b), np.cos(a+b)])
		A = np.array([[-L1*np.sin(a+b), -L1*np.sin(a+b)],
						[L1*np.cos(a+b), L2*np.cos(a+b)],
						[0  ,-L2*np.sin(b)],
						[0  , L2*np.cos(b)]])
		U,S,V = np.linalg.svd(A)
		print 'U:', U
		print 'V:',V
		print 'singulars:',S
		print np.hstack([v1-v2,v2])
		b1 = U.transpose().dot(np.hstack([v1-v2,v2]))
		print 'b1:',b1
		b11 = b1[:2]/S
		print 'b11:',b11
		da1,db1 = V.dot(b11)
		print 'new angular velosities:', da1,db1
		self.q_d = np.array([0,0,da1,db1])
		self.q[1] = 0
		

	def next_pos(self,tau):
		if self.q[1] > 0.: # flies
			self.q_d = self.next_flying_pos(tau)
			#print 'flying:',self.q, self.q_d
			self.q += tau * self.q_d
			if self.q[1] < 0: self.correct_state1()
				
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
		

	def is_down(self):
		_,y,a,b = self.q
		return y + L2*np.sin(b) < 0 or \
			   y + L2*np.sin(b) + 2*L1*np.sin(a+b) < 0



	def train(self, episode_len, episode_nbr, behavior='balance'):
		tau = 0.001
		speedup = 0.1
		self.pos_log = []
		for j in range(episode_nbr):			
			self.run_episode(episode_len,tau,behavior,'train')
			if (j+1)%100 == 0: print "%i episodes run" % (j+1)
	
		self.run_episode(episode_len,tau,behavior,'show')
		
		show(behavior+'.html',self.pos_log,tau/speedup)


	def run_episode(self, episode_len, tau, behavior, mode):
		t = 0
		reward = getattr(reinforce, self.reward_func[behavior])
		if mode == 'train': 
			self.init_randomly_standing()
			eps = EPS
		elif mode == 'show':
			self.psi = 0.2 
			self.q = np.array([0.4, 0., 1.5, 1.2])
			self.q_d = np.zeros(4)
			eps = 0.

		state = reinforce.get_state(self.psi, self.q, self.q_d)
		action = reinforce.get_policy(eps,state,self.Q[behavior])
		self.psi = reinforce.get_psi(state,action)
		i = 0
		while t < episode_len:
			t += tau
			i += 1
			if i%10 == 0: 
				next_state = reinforce.get_state(self.psi,self.q,self.q_d)
				rwd = reward(state,action,next_state,self.Q[behavior])
				if mode == 'train': reinforce.learn(self.Q[behavior],state,action,next_state,rwd)
				
				action = reinforce.get_policy(eps,next_state,self.Q[behavior])
				state = next_state
				self.psi = reinforce.get_psi(state,action)
				if mode == 'show': print "  action:",action

			if mode == 'show': 
				print "state:",state
				self.pos_log.append(tuple(self.q))
			
			self.next_pos(tau)
			
			if self.is_down(): 
				rwd = 0
				next_state = 'down'
				reinforce.learn(self.Q[behavior],state,action,next_state,rwd)
				break




