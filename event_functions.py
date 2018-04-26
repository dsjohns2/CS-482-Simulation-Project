import event
import random
import heapq
import numpy as np

# Helper Functions

san_fran_distance = 60 * 60


def gen_location():
    return (random.randint(0, san_fran_distance),
            random.randint(0, san_fran_distance))


def gen_end_rider(sys, start_loc):
    STD = 810 * sys.speed
    MEAN = 1663 * sys.speed
    # FIXME: don't cast dist to int (change everything else to floats instead)
    dist = max(1, int(np.random.randn() * STD + MEAN))
    delta_x = random.randint(-dist, dist)
    return (start_loc[0] + delta_x, start_loc[1] + (dist - delta_x) *
            -1 if random.randint(0, 1) == 0 else 1)


def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1])


def have_free_driver(sys):
    for driver in sys.driver_is_free:
        if driver:
            return True
    return False


def loc_rnd(sys):
    STD = 810 * sys.speed
    MEAN = 1663 * sys.speed
    return np.random.randn() * STD + MEAN


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
        "Rider Request", new_event_time, node_rider_request)
    eventlist_tuple = (new_event_time, new_event)
    heapq.heappush(sys.eventlist, eventlist_tuple)

    new_event_time = sys.cur_time
    new_event = event.event("Available Driver", new_event_time, node_available_driver, args={
                            'rider_id': rider_id, 'rider_location': rider_location})
    eventlist_tuple = (new_event_time, new_event)
    heapq.heappush(sys.eventlist, eventlist_tuple)

def node_available_driver(sys, args):
    rider_id = args["rider_id"]
    rider_location = args["rider_location"]
    if have_free_driver(sys):
        # State changes
        min_driver_id = None
        min_distance = None
        for driver_id, driver_loc in enumerate(sys.driver_current_locations):
            curr_distance = distance(rider_location, driver_loc)
            if sys.driver_is_free[driver_id] and \
                    (min_distance is None
                     or curr_distance < min_distance):
                min_driver_id = driver_id
                min_distance = curr_distance
        sys.driver_is_free[min_driver_id] = False

        # Schedule events
        new_event_time = sys.cur_time + min_distance/sys.speed
        # FIXME: Not sure if this is supposed to be higher or lower priority
        new_event = event.event(
            "Driver Response", new_event_time, node_driver_response,
            args={'rider_id': rider_id, 'driver_id': min_driver_id},
            priority=4)
        eventlist_tuple = (new_event_time, new_event)
        heapq.heappush(sys.eventlist, eventlist_tuple)
    else:
        sys.rider_queue.append(rider_id)


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
                            node_end_of_drive, args=args)
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
    new_event_time = sys.cur_time
    if len(sys.rider_queue) > 0:
        rider_id = sys.rider_queue.pop(0)
        rider_location = sys.rider_start_locations[rider_id]
        new_event = event.event("Available Driver", new_event_time, node_available_driver, args={
                                'rider_id': rider_id, 'rider_location': rider_location})
        eventlist_tuple = (new_event_time, new_event)
        heapq.heappush(sys.eventlist, eventlist_tuple)
