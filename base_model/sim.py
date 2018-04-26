from __future__ import print_function
import system
import event_functions
import heapq
import numpy as np
import random
import event

ic_num_drivers_list = [1, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
ic_speed = 20

num_times_run_sim = 1000
num_events_per_sim = 10000

for ic_num_drivers in ic_num_drivers_list:
	print("Running IC Drivers = " + str(ic_num_drivers))
	wait_times = []
	ride_times = []
	for i in range(0, num_times_run_sim):
		# Create system
		sys = system.system(num_drivers=ic_num_drivers, speed=ic_speed)

		# Set random seed
		np.random.seed(12345 - i*2)
		random.seed(12345 - i*2)

		# Schedule the initialization event
		initialization_event = event.event(
			"Initialize", 0, event_functions.node_init)
		event_tuple = (0, initialization_event)
		sys.eventlist.append(event_tuple)

		# This is the simulation loop
		event_num = 0
		while(event_num < num_events_per_sim):
			event_num += 1
			val, cur_event = heapq.heappop(sys.eventlist)
			sys.cur_time = cur_event.time
			cur_event.execute(sys)

		# Output data to analyze
		cur_sim_wait_times = []
		for start, end in zip(sys.rider_start_times, sys.rider_pickup_times):
			if(end != -1):
				cur_sim_wait_times.append(end - start)
		wait_times.append(cur_sim_wait_times)

		cur_sim_ride_times = []
		for start, end in zip(sys.rider_pickup_times, sys.rider_end_times):
			if(end != -1):
				cur_sim_ride_times.append(end - start)
		ride_times.append(cur_sim_ride_times)

	# Write wait times to file
	smallest_sim_len = len(wait_times[0])
	for i in range(0, len(wait_times)):
		if(len(wait_times[i]) < smallest_sim_len):
			smallest_sim_len = len(wait_times[i])

	import sys
	orig_stdout = sys.stdout
	f = open('basemodel_waittime_drivers'+str(ic_num_drivers)+'.csv', 'w')
	sys.stdout = f

	for i in range(0, smallest_sim_len):
		for j in range(0, len(wait_times)):
			print(wait_times[j][i], end=',')
		print("")

	sys.stdout = orig_stdout
	f.close()

	# Write ride times to file
	smallest_sim_len = len(ride_times[0])
	for i in range(0, len(ride_times)):
		if(len(ride_times[i]) < smallest_sim_len):
			smallest_sim_len = len(ride_times[i])

	import sys
	orig_stdout = sys.stdout
	f = open('basemodel_ridetime_drivers'+str(ic_num_drivers)+'.csv', 'w')
	sys.stdout = f

	for i in range(0, smallest_sim_len):
		for j in range(0, len(ride_times)):
			print(ride_times[j][i], end=',')
		print("")

	sys.stdout = orig_stdout
	f.close()
