from .solar_model import solar_model
from .inverter_model import inverter_model
from .state_machine import state_machine
from .fault_engine import fault_engine

class telemetry:
    def __init__(self):

        self.solar = solar_model()
        self.inverter = inverter_model()
        self.state_machine = state_machine()
        self.fault_engine = fault_engine()

        self.timestamp =0 #FIXME: decide the format/units of timestamp and adjust for hour->power calculation and STARTING state duration

        self.DC_power = 0
        self.DC_voltage = 0
        self.DC_current = 0

        self.AC_power = 0
        self.AC_voltage = 0
        self.AC_current = 0

        self.device_temp = 0
        self.todays_energy = 0

        self.current_state = "OFF"
        self.condition_status = "NO CONDITION"
        self.fault_status = "NO FAULT"


    def collect_data(self, timestamp): #FIXME
        self.timestamp = timestamp #FIXME

        self.condition_status = self.fault_engine.check_condition_status()
        self.fault_status = self.fault_engine.check_fault_status()

        multiplier = 0.2 if self.condition_status == "LOW IRRADIANCE" else 1

        self.DC_power = self.solar.get_panel_power(self.timestamp) * multiplier #FIXME
        self.DC_voltage = self.solar.get_panel_voltage()
        self.DC_current = self.DC_power/self.DC_voltage

        self.current_state = self.state_machine.change_state(self.DC_power, timestamp*3600) #FIXME



        if(self.fault_status=="NO FAULT" and self.current_state=="RUNNING"):

            self.AC_power = self.inverter.get_AC_output_power(self.DC_power)
            self.AC_voltage = self.inverter.get_AC_output_voltage()
            self.AC_current = self.inverter.get_AC_output_current()

        elif(self.fault_status=="NO FAULT" and self.current_state=="STARTING"):

            self.AC_power = 0
            self.AC_voltage = 0
            self.AC_current = 0
        else: #TODO: add conditions for faults

            self.DC_power = 0
            self.DC_voltage = 0
            self.DC_current = 0

            self.AC_power = 0
            self.AC_voltage = 0
            self.AC_current = 0

        self.device_temp = self.get_device_temperature()
        self.todays_energy = self.get_todays_energy()

        return {
            "timestamp": self.timestamp, #FIXME
            "dc_power": self.DC_power,
            "dc_voltage": self.DC_voltage,
            "dc_current": self.DC_current,
            "ac_power": self.AC_power,
            "ac_voltage": self.AC_voltage,
            "ac_current": self.AC_current,
            "device_temp": self.device_temp,
            "todays_energy": self.todays_energy,
            "current_state": self.current_state,
            "condition_status": self.condition_status,
            "fault_status": self.fault_status
        }



    def get_device_temperature(self):
        return 35 #TODO

    def get_todays_energy(self):
        return 0 #TODO
