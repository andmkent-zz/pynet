import sched

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