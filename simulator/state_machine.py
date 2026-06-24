
class state_machine:
    def __init__(self):
        self.OFF = "OFF"
        self.STARTING = "STARTING"
        self.RUNNING = "RUNNING"
        self.current_state = self.OFF

        self.start_threshold = 20
        self.start_init_time = -1
        self.fault_status = "NO FAULT"


    def change_state(self, panel_power, time, fault_status="NO FAULT"):
        self.fault_status = fault_status

        if(panel_power < self.start_threshold ):
            self.current_state = self.OFF

        elif(self.current_state == self.OFF and fault_status=="NO FAULT"):
            self.current_state = self.STARTING


        elif((self.current_state == self.STARTING and fault_status== "NO FAULT") or self.current_state == self.RUNNING):
            self.current_state = self.RUNNING

        return self.current_state

