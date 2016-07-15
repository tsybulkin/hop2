#
# Reinforcement learning module that provides
# an agent that learns different controls for various motions
#
import numpy as np


def get_state(q, q_d): 
	x,y,a,b = q
	dx,dy,da,db = q_d
	return (ro(10*y),ro(10*a),ro(10*b),ro(dx),ro(dy),ro(da),ro(db))


def get_psi(action): return (action-5)/10.


def get_policy(state,behavior='balance'): return get_random_action()


def get_random_action(excluded_actions=[]): 
	i = 0
	while i < 5:
		action = np.random.randint(0,11)
		if not action in excluded_actions: break
		i += 1
	return action


def learn(): pass


def ro(x): int(round(x))


#########  R E W A R D    F U N C T I O N S  ##########

def reward_balance(state,action,next_state,Q): return -1



def reward_hop(): return 0


def reward_salto(): return 0


