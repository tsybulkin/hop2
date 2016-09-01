from params import *
import numpy as np
import eqs, eqf
from show import show
import reinforce
from reinforce import reward_balance, reward_hop, reward_salto

EPS = 0.2


def run_wss(T, speedup=0.1, tau=0.001):
	bot = Robot()
	bot.q = np.array([0.4, 0., 1.7, 1.35]) 
	bot.psi = 0.5
	
	t = 0.
	while t < T:
		sim_time, action = bot.balance_policy(tau,0.2)
		bot.psi += action/10.
		print "action:",action,"bot state:",bot.q, bot.q_d
		
		[ bot.next_pos(tau) for _ in range(5)]
		t += tau*5

		bot.pos_log.append(tuple(bot.q))
		if bot.is_down(): break

	show('short_sims.html',bot.pos_log,tau/speedup)




def run(T, speedup=0.1, tau=0.001):
	assert tau < 0.1
	assert tau > 0
	assert T > 0

	bot = Robot()
	bot.q = np.array([0.6, 0., 2.8, 1.5]) # 
	bot.psi = 1.1
	"""
	bot.q = np.array([0.7, 0., 2.0, 1.255]) # salto settings
	bot.psi = 0.9
	"""
	t = 0.
	while t < T:
		#bot.psi = get_psi(get_policy(EPS,bot.q,bot.q_d))
		bot.next_pos(tau)
		t += tau
		bot.pos_log.append(tuple(bot.q))
		if bot.is_down(): break

	show('no_control.html',bot.pos_log,tau/speedup)


class Robot():
	def __init__(self,x=0.3, y=0., a=1.8, b=1.3):
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


	def fly_to_stand(self):
		a,b = self.q[2:]
		vx,vy,va,vb = self.q_d
		A = np.array([ [-L1*np.sin(a+b), -(L2*np.sin(b)+L1*np.sin(a+b)) ],
						[L1*np.cos(a+b),  (L2*np.cos(b)+L1*np.cos(a+b))]])
		C = np.array([vx,vy])

		da,db = np.linalg.inv(A).dot(C)
		print "da, db:", da,db
		self.q_d = np.array([0.,0.,da+va,db+vb])
		print "q_d:",self.q_d
		self.q[1] = 0.
		
		if abs(da+va) > 100 or abs(db+vb) > 100: return False
		else: return True
		

	def correct_state(self):
		x,y,a,b = self.q
		dx,dy,da,db = self.q_d
		#print 'velosities:',self.q_d
		v2 = np.array([dx,dy]) + L2*db*np.array([-np.sin(b), np.cos(b)])
		v1 = v2 + L1*(da+db)*np.array([-np.sin(a+b), np.cos(a+b)])
		
		da1 = np.cross(np.array([np.cos(a+b),np.sin(a+b)]), v1) / L1
		db1 = np.cross(np.array([np.cos(b),np.sin(b)]), v2) / L2

		#print 'new angular velosities:', da1,db1
		self.q_d[0] = 0
		self.q_d[1] = 0
		self.q_d[2] = da1
		self.q_d[3] = db1
		
		self.q[1] = 0
		
		if abs(da1) > 100 or abs(db1) > 100: return False
		else: return True
		
	def copy(self):
		b = Robot()
		b.q = self.q.copy()
		b.q_d = self.q_d.copy()
		b.psi = self.psi
		return b


	def next_pos(self,tau):
		if self.q[1] > 0.: # flies
			self.q_d = self.next_flying_pos(tau)
			self.q += tau * self.q_d
			print 'q:', self.q, '  q_d:', self.q_d
			
			if self.q[1] < 0.: return self.fly_to_stand() #self.correct_state()
			else: return True
				
		else: # stands
			qd_s = self.next_standing_pos(tau)
			qd_f = self.next_flying_pos(tau)
			print 'qd_s:', qd_s, '  q_df:', qd_f
				
			if qd_f[1] > self.q[1]: self.q_d = qd_f
			else: self.q_d = qd_s
			
			self.q += tau * self.q_d
			return True
		

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
			
	
	def is_down(self): ## if robot fell down
		_,y,a,b = self.q
		return y + L2*np.sin(b) + 2*L1*np.sin(a+b) < 0 or \
			   y + L2*np.sin(b) < 0 or \
			   a > 3.1 or a < 0.

	def fell_on_back(self):
		_,y,a,b = self.q
		if b <= 0.: return True
		return False


	def balance_policy(self,tau,T):
		b_times = [ (abs(self.get_Vx(action,tau,T)),action) for action in [-1,0,1]]
		print b_times

		return min(b_times)


	def get_Vx(self,action,tau,T):
		botc = self.copy()
		botc.psi += action/10.
		if abs(botc.psi) >= 1.: return np.inf

		t = 0.
		while t < T:
			t += tau
			if not botc.next_pos(tau): 
				print "too large load duirng landing"
				return np.inf			
			if botc.is_down():
				if botc.fell_on_back(): print "fell on back"
				else: print "fell forward"
				break
		da,db = botc.q_d[2:]
		a,b = botc.q[2:]
		return -L2*db*np.sin(b) - L1*(da+db)*np.sin(a+b)


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
		reward = getattr(reinforce, self.reward_func[behavior]) # rewarding function
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
				#if mode == 'show': print "  action:",action

			if mode == 'show': 
				#print "state:",state
				self.pos_log.append(tuple(self.q))
			
			if not self.next_pos(tau): 
				print "too large load duirng landing"
				rwd = -10
				next_state = 'down'
				reinforce.learn(self.Q[behavior],state,action,next_state,rwd)
				break
			
			if self.is_down(): 
				rwd = 0
				next_state = 'down'
				reinforce.learn(self.Q[behavior],state,action,next_state,rwd)
				break




