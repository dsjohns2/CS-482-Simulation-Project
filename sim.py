import event
import system
import event_functions

# Schedule the initialization event.
sys = system.system()
initialization_event = event.event(0, event_functions.node_init)
sys.eventlist.append(initialization_event)

# This is the simulation loop.
for event in sys.eventlist:
	event.execute(sys)
