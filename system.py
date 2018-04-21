class system:
    def __init__(self, num_drivers=5):
        # Event list
        self.eventlist = []

        # System Variables
        self.cur_time = 0
        self.rider_start_locations = []
        self.rider_end_locations = []
        self.rider_start_times = []
        self.rider_end_times = []
        self.num_drivers = num_drivers
        self.driver_is_free = []
        self.driver_current_locations = []
