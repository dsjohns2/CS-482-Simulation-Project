import event

# These are the nodes in the event graph.
def node_init(ev_list):
	print("This is the initialization event.")

	# State changes

	# Schedule events
	new_event = event.event(1, node_rider_request)
	sys.eventlist.append(new_event)
	
def node_rider_request(ev_list):
	print("This is the rider request event.")

	# State changes

	# Schedule events
	new_event = event.event(7, node_rider_request)
	ev_list.append(new_event)
	new_event = event.event(7, node_driver_response)
	ev_list.append(new_event)

def node_driver_response(ev_list):
	print("This is the driver response event.")

	# State changes

	# Schedule events
	new_event = event.event(7, node_end_of_drive)
	ev_list.append(new_event)

def node_end_of_drive(ev_list):
	print("This is the end of drive event.")

	# State changes

	# Schedule events
	new_event = event.event(7, node_driver_response)
	ev_list.append(new_event)
