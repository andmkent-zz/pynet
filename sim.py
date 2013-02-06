import sched
import Queue
import random
import sys
import math



class Environment:
	
	def __init__(self, msg_size, link_bw, link_len):
		self.msg_size = msg_size # bits
		self.link_bw = link_bw # bits/s
		self.link_len = link_len # meters
		self.e = 200000000 # m/s


def run_model(load_ratio):
	s = Scheduler()
	env = Environment(msg_size=1000.0, link_bw=1000000.0, link_len=300000.0) 
	l = Link(name='link', scheduler=s, environment=env)
	n1 = Node(name='one', link=l)
	g = Generator(scheduler=s, node=n1, load=load_ratio, environment=env, duration=100)
	s.add(time=s.current_time(), event='generate', handler=g.handle)
	s.run()

if __name__ == '__main__':
	stdout = sys.stdout
	sys.stdout = open('lab1-all.rdata', 'w')
	for n in range(0, 10):
		n += .01
		run_model(n * 10 / 100.0)
	
	run_model(.95)
		
	sys.stdout.close()
	sys.stdout = stdout
	
	
	
