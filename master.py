from multiprocessing import Pool, Process, Pipe, Queue
from time import sleep
from math import log
import numpy as np
import sys


def worker(pid, master_conn, q, T, N):
	for i in xrange(N):
		#sleep(np.random.random())
		q.put((pid,'req',log(i+1) ))
	q.put((pid,'done'))


def start_Qserver(workers,queue):
	for pid in workers.keys():
		workers[pid]['proc'].start()

	while len(workers) > 0:
		msg = queue.get()
		if msg[1] == 'done':
			pid = msg[0]
			workers[pid]['proc'].join()
			workers.pop(pid)
			print 'worker %i has finished. %i workers is still working' % (pid, len(workers))

		elif msg[1] == 'req': print 'get',msg[2]

		elif msg[1] == 'update': pass

		else: raise

	print 'All workers finished. Exiting ...'


def main(T,N):
	q = Queue()
	p_nbr = 5

	workers = {}

	for i in range(p_nbr):
		pipe = Pipe()
		p = Process(target=worker, args=(i, pipe, q, T, N/p_nbr) )
		workers[i] = {'id':i, 'pipe':pipe, 'proc':p}
		
	start_Qserver(workers,q)

	
if __name__ == "__main__":
	T = float(sys.argv[1])
	N = int(sys.argv[2])
	print sys.argv[1:3]
	main(T,N)