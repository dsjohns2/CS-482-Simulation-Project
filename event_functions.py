import event
import system

# These are the nodes in the event graph.
def node_init(sys):
	print("This is the initialization event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time + 1
	new_event = event.event("Rider Request", new_event_time, node_rider_request)
	sys.eventlist.append(new_event)
	
def node_rider_request(sys):
	print("This is the rider request event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time + 1
	new_event = event.event("Rider Request", new_event_time, node_rider_request)
	sys.eventlist.append(new_event)

	new_event_time = sys.cur_time + 1
	new_event = event.event("Driver Response", new_event_time, node_driver_response)
	sys.eventlist.append(new_event)

def node_driver_response(sys):
	print("This is the driver response event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time + 1
	new_event = event.event("End of Drive", new_event_time, node_end_of_drive)
	sys.eventlist.append(new_event)

def node_end_of_drive(sys):
	print("This is the end of drive event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time + 1
	new_event = event.event("Driver Response", new_event_time, node_driver_response)
	sys.eventlist.append(new_event)
