import numpy as np
import random


class system:
    def __init__(self, num_drivers=5, self_driving=True, speed=10):
        # Event list
        self.eventlist = []

        # System Variables
        self.cur_time = 0
        self.rider_queue = []
        self.rider_start_locations = []
        self.rider_end_locations = []
        self.rider_start_times = []
        self.rider_pickup_times = []
        self.rider_end_times = []
        self.num_drivers = num_drivers
        self.driver_is_free = []
        self.driver_current_locations = []
        self.speed = speed
        np.random.seed(12345)
        random.seed(12345)
