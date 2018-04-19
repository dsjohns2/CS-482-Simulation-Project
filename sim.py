import event
import system
import event_functions

# Schedule the initialization event.
sys = system.system()
initialization_event = event.event(0, "Initialize", event_functions.node_init)
sys.eventlist.append(initialization_event)

# This is the simulation loop.
for event_num, event in enumerate(sys.eventlist):
	event.execute(sys)
	if(event_num > 5):
		break
