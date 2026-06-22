
class state_machine:
    def __init__(self):
        self.OFF = "OFF"
        self.STARTING = "STARTING"
        self.RUNNING = "RUNNING"
        self.current_state = self.OFF

        self.start_threshold = 100
        self.start_init_time = -1

        self.start_duration = 5 #TODO: find out what the time formatting will look like

    def change_state(self, panel_power, time):

        if(panel_power < self.start_threshold ):
            self.current_state = self.OFF
            self.start_init_time = -1

        elif(self.current_state == self.OFF):
            self.current_state = self.STARTING
            self.start_init_time = time

        elif(self.current_state == self.STARTING and time -self.start_init_time <self.start_duration):
            self.current_state = self.STARTING

        elif(self.current_state == self.STARTING or self.current_state == self.RUNNING):
            self.current_state = self.RUNNING


        return self.current_state

