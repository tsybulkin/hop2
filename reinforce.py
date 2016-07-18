#
# Reinforcement learning module that provides
# an agent that learns different controls for various motions
#
import numpy as np
import operator

GAMA = 0.95
ALPHA = 0.25


def get_state(psi, q, q_d): 
	x,y,a,b = q
	dx,dy,da,db = q_d
	return (psi,ro(5*y),ro(5*a),ro(5*b),ro(dx),ro(dy),ro(da/2),ro(db/2))

def get_state_value(state,Q):
	if state == 'down': return -10
	values = Q.get(state,{'unknown':2})
	return max(values.iteritems(), key=operator.itemgetter(1))[1]


def get_psi(state,action): return state[0] + action/5.
	

def get_policy(eps,state,Q): 
	if np.random.random() < eps: return get_random_action(state)
	else: return get_best_learned_action(state,Q)



def get_best_learned_action(state, Q):
	values = Q.get(state, None )
	if values == None: return get_random_action(state)
	
	Ac,V = max(values.iteritems(), key=operator.itemgetter(1))
	if V < 2: return get_random_action(state) 
	else: return Ac
	

def get_random_action(state): 
	psi = state[0]
	if psi == -1.: return np.random.randint(0,2)
	elif psi == 1.: return np.random.randint(-1,1)
	else: return np.random.randint(-1,2)
	

def learn(Q,state,action,next_state,reward): 
	V1 = get_state_value(next_state,Q)
	values = Q.get(state,None)
	if values == None: 
		Q[state] = {action: GAMA*V1+reward}
	else:
		V = values.get(action,0)
		values[action] = (1-ALPHA)*V + ALPHA*(V1*GAMA + reward)
		

def ro(x): return int(round(x))


#########  R E W A R D    F U N C T I O N S  ##########

def reward_balance(state,action,next_state,Q): return 1 - 0.2*abs(action)


def reward_hop(): return 0


def reward_salto(): return 0


