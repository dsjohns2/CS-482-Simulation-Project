class event:
    def __init__(self, name, time, func, args={}, priority=5):
        self.name = name
        self.time = time
        self.func = func
        self.args = args
        self.priority = priority

    def execute(self, sys):
        self.func(sys, self.args)

    def __lt__(self, event_b):
        '''
        Needed for tie breaking. Compares priority of the events.
        Lower value means higher priority.
        '''
        return self.priority < event_b.priority
