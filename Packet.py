class Packet:
    
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
#        values.append(str(self.tx))
#        values.append(' => ')
#        values.append(str(self.rx))
#        values.append(' ')
#        values.append(str(self.load))
#        values.append(' ')
        values.append(str(self.util))
        values.append(' ')
        values.append(str(self.tx_delay))
        values.append(' ')
        values.append(str(self.prop_delay))
        values.append(' ')
#        values.append(str(self.nq_time))
#        values.append(' ')
#        values.append(str(self.dq_time))
#        values.append(' ')
        values.append(str(self.dq_time - self.nq_time))
        return ''.join(values)