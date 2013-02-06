import sched
import Queue
import random
import sys
import math

class Scheduler:
    current = 0
    
    def __init__(self):
        self.current = 0
        self.scheduler = sched.scheduler( \
			Scheduler.current_time, \
			Scheduler.advance_time)
    
    @staticmethod
    def current_time():
        return Scheduler.current

    @staticmethod
    def advance_time(units):
        Scheduler.current += units

    def add(self,time,event,handler):
       return self.scheduler.enterabs(time,1,handler,[time,event])

    def cancel(self,event):
        self.scheduler.cancel(event)

    def run(self):
        self.scheduler.run()

class Environment:
	
	def __init__(self, msg_size, link_bw, link_len):
		self.msg_size = msg_size # bits
		self.link_bw = link_bw # bits/s
		self.link_len = link_len # meters
		self.e = 200000000 # m/s

class Message:
	
	def __init__(self, src, dst):
		self.tx = src
		self.rx = dst
		self.tx_delay = -1
		self.prop_delay = -1
		self.nq_time = -1
		self.dq_time = -1
		self.load = -1
		self.util = -1
	
	# Load TxDelay PropDelay QueueEnter QueueExit QueueDuration
	def details(self):
		values = []
#		values.append(str(self.tx))
#		values.append(' => ')
#		values.append(str(self.rx))
#		values.append(' ')
#		values.append(str(self.load))
#		values.append(' ')
		values.append(str(self.util))
		values.append(' ')
		values.append(str(self.tx_delay))
		values.append(' ')
		values.append(str(self.prop_delay))
		values.append(' ')
#		values.append(str(self.nq_time))
#		values.append(' ')
#		values.append(str(self.dq_time))
#		values.append(' ')
		values.append(str(self.dq_time - self.nq_time))
		return ''.join(values)
		
		
class Node:

	def __init__(self, name, link):
		self.name = name
		self.link = link
	
	def handle_message(self, t, message):
		message.nq_time = t
		self.link.enqueue(t, message)

class Link:
	
	def __init__(self, name, scheduler, environment):
		self.s = scheduler
		self.msgLog = []
		self.name = name
		self.env = environment
		self.q = Queue.Queue()

	def tx_handler(self,t,message):
		# if queue empty, no-op
		if self.q.empty():
			return
		
		# else grab from queue
		msg = self.dequeue(t)
		
		# calculate txDelay
		tx_time = self.env.msg_size / self.env.link_bw
		msg.tx_delay = tx_time
		tx_time += t
		
		# schedule packet for PropHandler at now + txDelay
		self.s.add(time=tx_time, \
			event=msg, \
			handler=self.prop_handler)
			
		# if any other packets in queue
		#   schedule self to grab another packet at now + txDelay
		self.s.add(time=tx_time, \
			event=0, \
			handler=self.tx_handler)

	def prop_handler(self, t, msg):
		#calc & set propDelay
		propDelay = self.env.link_len / self.env.e
		msg.prop_delay = propDelay
		propDelay += t
		#schedule logging msg after propDelay
		self.s.add(time=propDelay, \
			event=msg, \
			handler=self.log_msg)
	
	def log_msg(self,t,msg):
		print(msg.details())

	def enqueue(self, t, msg):
		empty = self.q.empty()
		self.q.put(msg)
		if empty:
			self.s.add(time=t + .0001, \
				event=0, \
				handler=self.tx_handler)
		
	def dequeue(self, t):
		msg = self.q.get()
		msg.dq_time = t
		return msg
	

class Generator:
    def __init__(self,node,scheduler,load, environment, duration):
        self.start = Scheduler.current_time()
        self.scheduler = scheduler
        self.util = load
        self.mean_load = load * environment.link_bw / environment.msg_size
        self.duration = duration
        self.node = node

    def exponential(self, beta):
		return -beta * math.log(1.0 - random.random())

    def handle(self,now,event):
        if event == 'generate':
            if (now - self.start) > self.duration:
                return
                
            message = Message(src=self.node.name, dst='null')
            message.load = self.mean_load
            message.util = self.util
            self.scheduler.add(time=now, event=message, handler=self.node.handle_message)
            now += random.expovariate(self.mean_load)
            self.scheduler.add(time=now, event='generate', handler=self.handle)



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
	
	
	
