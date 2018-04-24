import event
import random
import system
import heapq

# Helper Functions


def gen_location():
    return random.randint(0, 100)


def distance(a, b):
    return abs(a-b)


def have_free_driver(sys):
    for driver in sys.driver_is_free:
        if driver:
            return True
    return False


# These are the nodes in the event graph.


def node_init(sys, args):
    print("This is the initialization event.")
    print("Time: " + str(sys.cur_time))
    print("")

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
    print("This is the rider request event.")
    print("Time: " + str(sys.cur_time))

    # State changes
    rider_id = len(sys.rider_start_locations)
    rider_location = gen_location()
    sys.rider_start_locations.append(rider_location)
    sys.rider_end_locations.append(-1)
    sys.rider_start_times.append(sys.cur_time)
    sys.rider_end_times.append(-1)

    # Schedule events
    new_event_time = sys.cur_time + 10
    new_event = event.event(
        "Rider Request", new_event_time, node_rider_request)
    eventlist_tuple = (new_event_time, new_event)
    heapq.heappush(sys.eventlist, eventlist_tuple)

    new_event_time = sys.cur_time
    new_event = event.event("Available Driver", new_event_time, node_available_driver, args={
                            'rider_id': rider_id, 'rider_location': rider_location})
    eventlist_tuple = (new_event_time, new_event)
    heapq.heappush(sys.eventlist, eventlist_tuple)

    print("")


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
        print("Driver {} is taking request from rider {}"
              .format(min_driver_id, rider_id))

        # Schedule events
        new_event_time = sys.cur_time + 15
        # FIXME: Not sure if this is supposed to be higher or lower priority
        new_event = event.event(
            "Driver Response", new_event_time, node_driver_response,
            args={'rider_id': rider_id, 'driver_id': min_driver_id},
            priority=4)
        eventlist_tuple = (new_event_time, new_event)
        heapq.heappush(sys.eventlist, eventlist_tuple)


def node_driver_response(sys, args):
    print("This is the driver response event.")
    print("Time: " + str(sys.cur_time))
    print("")

    # State changes
    driver_id = args['driver_id']
    rider_id = args['rider_id']
    sys.driver_current_locations[driver_id] = sys.rider_start_locations[rider_id]

    # Schedule events
    new_event_time = sys.cur_time + 20
    new_event = event.event("End of Drive", new_event_time,
                            node_end_of_drive, args=args)
    eventlist_tuple = (new_event_time, new_event)
    heapq.heappush(sys.eventlist, eventlist_tuple)


def node_end_of_drive(sys, args):
    print("This is the end of drive event.")
    print("Time: " + str(sys.cur_time))

    # State changes
    driver_id = args['driver_id']
    rider_id = args['rider_id']
    rider_location = sys.rider_end_locations[rider_id]
    sys.rider_end_times[rider_id] = sys.cur_time
    sys.driver_is_free[driver_id] = True
    sys.driver_current_locations[driver_id] = rider_location

    print("Rider Spent {} minutes in the system".format(
        sys.rider_end_times[rider_id] - sys.rider_start_times[rider_id]))

    # Schedule events
    new_event_time = sys.cur_time
    new_event = event.event("Available Driver", new_event_time, node_available_driver, args={
                            'rider_id': rider_id, 'rider_location': rider_location})
    eventlist_tuple = (new_event_time, new_event)
    heapq.heappush(sys.eventlist, eventlist_tuple)
    print("")
