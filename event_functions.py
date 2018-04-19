import event
import system
import heapq

# These are the nodes in the event graph.
def node_init(sys):
	print("This is the initialization event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time
	new_event = event.event("Rider Request", new_event_time, node_rider_request)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)
	
def node_rider_request(sys):
	print("This is the rider request event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time + 10
	new_event = event.event("Rider Request", new_event_time, node_rider_request)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)

	new_event_time = sys.cur_time + 15
	new_event = event.event("Driver Response", new_event_time, node_driver_response)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)

def node_driver_response(sys):
	print("This is the driver response event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time + 20
	new_event = event.event("End of Drive", new_event_time, node_end_of_drive)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)

def node_end_of_drive(sys):
	print("This is the end of drive event.")
	print("Time: " + str(sys.cur_time))
	print("")

	# State changes

	# Schedule events
	new_event_time = sys.cur_time
	new_event = event.event("Driver Response", new_event_time, node_driver_response)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)
