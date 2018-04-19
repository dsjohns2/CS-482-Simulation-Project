import event
import system
import event_functions
import heapq

# Schedule the initialization event.
sys = system.system()
initialization_event = (0, event.event("Initialize", 0, event_functions.node_init))
sys.eventlist.append(initialization_event)

# This is the simulation loop.
event_num = 0
while(event_num < 15):
	event_num += 1
	val, event = heapq.heappop(sys.eventlist)
	sys.cur_time = event.time
	event.execute(sys)
