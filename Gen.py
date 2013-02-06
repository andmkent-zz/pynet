import random
import Packet
import math


class Generator:
    def __init__(self,node,scheduler,load, environment, duration):
        self.start = scheduler.current_time()
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
                
            packet = Packet(src=self.node.name, dst='null')
            packet.load = self.mean_load
            packet.util = self.util
            self.scheduler.add(time=now, event=packet, handler=self.node.handle_message)
            now += random.expovariate(self.mean_load)
            self.scheduler.add(time=now, event='generate', handler=self.handle)
