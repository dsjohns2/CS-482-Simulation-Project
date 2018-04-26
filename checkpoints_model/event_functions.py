import event
import random
import heapq
import numpy as np

# Helper Functions

san_fran_distance = 60 * 60


def gen_location():
	return (random.uniform(0, san_fran_distance),
			random.uniform(0, san_fran_distance))


def gen_end_rider(sys, start_loc):
	STD = 810 * sys.speed
	MEAN = 1663 * sys.speed
	# FIXME: don't cast dist to int (change everything else to floats instead)
	dist = max(1, int(np.random.randn() * STD + MEAN))
	delta_x = random.uniform(-dist, dist)
	return (start_loc[0] + delta_x, start_loc[1] + (dist - delta_x) *
			-1 if random.uniform(0, 1) == 0 else 1)


def distance(a, b):
	return abs(a[0]-b[0]) + abs(a[1] - b[1])


def have_free_driver(sys):
	for driver in sys.driver_is_free:
		if driver:
			return True
	return False


def inter_rnd():
	STD = 10
	MEAN = 60
	return np.random.randn() * STD + MEAN


# These are the nodes in the event graph.


def node_init(sys, args):
	# State changes
	for i in range(sys.num_drivers):
		sys.driver_current_locations.append(gen_location())
		sys.driver_is_free.append(True)
		sys.drivers_free_at_last_update.append(True)

	# Schedule events
	new_event_time = sys.cur_time
	new_event = event.event(
		"Rider Request", new_event_time, node_rider_request)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)

def node_rider_request(sys, args):
	# State changes
	rider_id = len(sys.rider_start_locations)
	rider_location = gen_location()
	sys.rider_start_locations.append(rider_location)
	sys.rider_end_locations.append(gen_end_rider(sys, rider_location))
	sys.rider_start_times.append(sys.cur_time)
	sys.rider_pickup_times.append(-1)
	sys.rider_end_times.append(-1)

	# Schedule events
	new_event_time = sys.cur_time + inter_rnd()
	new_event = event.event(
		"Rider Request", new_event_time, node_rider_request, priority=5)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)

	new_event_time = sys.cur_time
	new_event = event.event("Update Driver Location", new_event_time, node_update_driver_locations, args={'rider_id': rider_id, 'rider_location': rider_location}, priority=1)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)

def node_update_driver_locations(sys, args):
	# State changes
	checkpoint = (1800, 1800)
	time_diff = sys.cur_time - sys.last_update
	dist_diff = time_diff * sys.speed
	# Update driver locations that might be moving to checkpoints
	for driver_id in range(0, len(sys.drivers_free_at_last_update)):
		if(sys.drivers_free_at_last_update[driver_id]):
			# Move driver closer to checkpoint in x direction
			cur_x = sys.driver_current_locations[driver_id][0]
			cur_y = sys.driver_current_locations[driver_id][1]
			x_diff = checkpoint[0] - cur_x
			if(abs(x_diff) > dist_diff):
				# All movement is in x direction
				sys.driver_current_locations[driver_id] = (cur_x + dist_diff * np.sign(x_diff), cur_y)
			else:
				# Some movement in y direction
				rem_dist_to_move = dist_diff - abs(x_diff)
				y_diff = checkpoint[1] - sys.driver_current_locations[driver_id][1]
				if(abs(y_diff) > rem_dist_to_move):
					# Move some toward checkpoint
					sys.driver_current_locations[driver_id] = (cur_x + x_diff, cur_y + rem_dist_to_move * np.sign(y_diff))
				else:
					# Move all the way to checkpoint
					sys.driver_current_locations[driver_id] = (cur_x + x_diff, cur_y + y_diff)
			
	sys.drivers_free_at_last_update = sys.driver_is_free
	sys.last_update = sys.cur_time

	# Schedule events
	new_event_time = sys.cur_time
	new_event = event.event("Available Driver", new_event_time, node_available_driver, args=args, priority=2)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)

def node_available_driver(sys, args):
	# State changes
	rider_id = args["rider_id"]
	rider_location = args["rider_location"]
	free_driver = have_free_driver(sys)
	min_driver_id = None
	min_distance = None
	if free_driver:
		for driver_id, driver_loc in enumerate(sys.driver_current_locations):
			curr_distance = distance(rider_location, driver_loc)
			if sys.driver_is_free[driver_id] and \
					(min_distance is None
					 or curr_distance < min_distance):
				min_driver_id = driver_id
				min_distance = curr_distance
		sys.driver_is_free[min_driver_id] = False
	else:
		sys.rider_queue.append(rider_id)

	# Schedule events
	if free_driver:
		new_event_time = sys.cur_time + min_distance/sys.speed
		new_event = event.event("Driver Response", new_event_time, node_driver_response, args={'rider_id': rider_id, 'driver_id': min_driver_id}, priority=3)
		eventlist_tuple = (new_event_time, new_event)
		heapq.heappush(sys.eventlist, eventlist_tuple)


def node_driver_response(sys, args):
	# State changes
	driver_id = args['driver_id']
	rider_id = args['rider_id']
	sys.driver_current_locations[driver_id] = sys.rider_start_locations[rider_id]
	sys.rider_pickup_times[rider_id] = sys.cur_time
	drive_dist = distance(
		sys.rider_start_locations[rider_id], sys.rider_end_locations[rider_id])

	# Schedule events
	new_event_time = sys.cur_time + drive_dist/sys.speed
	new_event = event.event("End of Drive", new_event_time,
							node_end_of_drive, args=args, priority=4)
	eventlist_tuple = (new_event_time, new_event)
	heapq.heappush(sys.eventlist, eventlist_tuple)


def node_end_of_drive(sys, args):
	# State changes
	driver_id = args['driver_id']
	rider_id = args['rider_id']
	rider_location = sys.rider_end_locations[rider_id]
	sys.rider_end_times[rider_id] = sys.cur_time
	sys.driver_is_free[driver_id] = True
	sys.driver_current_locations[driver_id] = rider_location

	# Schedule events
	if len(sys.rider_queue) > 0:
		rider_id = sys.rider_queue.pop(0)
		rider_location = sys.rider_start_locations[rider_id]
		new_event_time = sys.cur_time
		new_event = event.event("Update Driver Location", new_event_time, node_update_driver_locations, args={'rider_id': rider_id, 'rider_location': rider_location}, priority=1)
		eventlist_tuple = (new_event_time, new_event)
		heapq.heappush(sys.eventlist, eventlist_tuple)

