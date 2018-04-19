import event

# These are the nodes in the event graph.
def node_init(ev_list):
	# State changes
	print("This is the initialization event.")

	# Schedule events
	new_event = event.event(1, node_rider_request)
	ev_list.append(new_event)
	
def node_rider_request(ev_list):
	# State changes
	print("This is the rider request event.")

	# Schedule events
	new_event = event.event(7, node_rider_request)
	ev_list.append(new_event)

def node_driver_response(ev_list):
	# State changes
	print("This is the driver response event.")

	# Schedule events

def node_end_of_drive(ev_list):
	# State changes
	print("This is the end of drive event.")

	# Schedule events

