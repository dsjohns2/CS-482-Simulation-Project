import event
import eventlist
import event_functions

# Variables

# This schedules the initialization event.
ev = eventlist.eventlist()
initialization_event = event.event(0, event_functions.node_init)
ev.eventlist.append(initialization_event)

# This is the simulation loop.
for event in ev.eventlist:
	event.execute(ev.eventlist)
