
import Queue

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