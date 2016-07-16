#
# Reinforcement learning module that provides
# an agent that learns different controls for various motions
#
import numpy as np
import operator

GAMA = 0.95
ALPHA = 0.25
EPS = 0.1

def get_state(q, q_d): 
	x,y,a,b = q
	dx,dy,da,db = q_d
	return (ro(10*y),ro(10*a),ro(10*b),ro(dx),ro(dy),ro(da),ro(db))

def get_state_value(state,Q):
	values = Q.get(state,{'any':2})
	return max(values.iteritems(), key=operator.itemgetter(1))[1]


def get_psi(action): return (action-5)/10.


def get_policy(state,Q): 
	if np.random.random() < EPS: return get_random_action()
	else: return get_best_learned_action(state,Q)



def get_best_learned_action(state, Q):
	values = Q.get(state, {get_random_action():0} )
	return max(values.iteritems(), key=operator.itemgetter(1))[0]
	

def get_random_action(excluded_actions=[]): 
	i = 0
	while i < 5:
		action = np.random.randint(0,11)
		if not action in excluded_actions: break
		i += 1
	return action


def learn(Q,state,action,next_state,reward): 
	V1 = get_state_value(next_state,Q)
	values = Q.get(state,{})
	if values == {}: 
		Q[state] = {action: GAMA*V1+reward}
	else:
		V = values.get(action,0)
		values[action] = (1-ALPHA)*V + ALPHA*(V1*GAMA + reward)
		

def ro(x): return int(round(x))


#########  R E W A R D    F U N C T I O N S  ##########

def reward_balance(state,action,next_state,Q): return 1


def reward_hop(): return 0


def reward_salto(): return 0


