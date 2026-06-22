from inverter_model import  *
from solar_model import *
class state_machine:
    def __init__(self):
        self.OFF = "OFF"
        self.STARTING = "STARTING"
        self.RUNNING = "RUNNING"
        current_state = self.OFF()



    def get_current_state(self):
        return self.current_state;

    def OFF(self):
        self.DC_voltage, self.DC_power, self.DC_current = 0, 0, 0
        self.AC_voltage, self.AC_power, self.AC_current = 0, 0, 0
        self.Device_temp = -1 #FIXME
        self.current_state = self.OFF
        return "OFF"

    def STARTING(self):
        self.DC_voltage, self.DC_power, self.DC_current = 0, 0, 0
        self.AC_voltage, self.AC_power, self.AC_current = 0, 0, 0
        self.Device_temp = 0 #FIXME
        self.current_state = self.STARTING
        return "STARTING"

    def RUNNING(self):
        self.DC_power = solar_model.get_panel_power()
        self.DC_voltage = solar_model.get_panel_voltage()
        self.DC_current = solar_model.get_panel_current()

        self.AC_voltage = inverter_model.get_AC_output_voltage()
        self.AC_power = inverter_model.get_AC_output_power()
        self.AC_current = inverter_model.get_AC_output_current()

        self.Device_temp = 0 #FIXME

        self.current_state = self.RUNNING
        return "RUNNING"


    def change_state(self): #TODO: manage changing of states
        if(self.get_current_state() == "OFF"):
            pass
