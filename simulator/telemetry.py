from .solar_model import solar_model
from .inverter_model import inverter_model
from .state_machine import state_machine
from .fault_engine import fault_engine
import random

class telemetry:
    def __init__(self):

        self.solar = solar_model()
        self.inverter = inverter_model()
        self.state_machine = state_machine()
        self.fault_engine = fault_engine()

        self.timestamp =0 #fixed: timestamp is in minutes

        self.irradiance = 0

        self.DC_power = 0
        self.DC_voltage = 0
        self.DC_current = 0

        self.AC_power = 0
        self.AC_voltage = 0
        self.AC_current = 0

        self.todays_energy = 0

        self.current_state = "OFF"
        self.condition_status = "NO CONDITION"
        self.fault_status = "NO FAULT"

        self.grid_failure_imminence = -1 #number of simulated minutes until grid_failure


    def collect_data(self, timestamp): #in minutes
        self.timestamp = timestamp #in minutes

        self.condition_status = self.fault_engine.check_condition_status()
        self.fault_status = self.fault_engine.check_fault_status()

        multiplier = 0.2 if self.condition_status == "LOW IRRADIANCE" else 1

        self.irradiance = self.solar.set_panel_irradiance(self.timestamp)

        self.DC_power = round(self.solar.get_panel_power() * multiplier)
        self.DC_voltage = self.solar.get_panel_voltage()
        self.DC_current = self.DC_power/self.DC_voltage

        if(not (self.fault_status=="GRID FAILURE" and self.current_state =="OFF")):
            self.current_state = self.state_machine.change_state(self.DC_power, timestamp*60, self.fault_status) #FIXME: make it minutes to keep consistency
        if(self.fault_status=="GRID FAILURE"):
            self.AC_power = self.inverter.get_AC_output_power(self.DC_power)
            self.AC_voltage = self.inverter.set_AC_output_voltage(self.AC_voltage - random.randint(5, 10)) #FIXME


        if(self.fault_status=="NO FAULT" and self.current_state=="RUNNING"):

            self.AC_power = self.inverter.get_AC_output_power(self.DC_power)
            self.AC_voltage = self.inverter.set_AC_output_voltage(random.randint(227,237)) #FIXME
            self.AC_voltage = self.inverter.get_AC_output_voltage()
            self.AC_current = self.inverter.get_AC_output_current()

        elif(self.fault_status=="NO FAULT" and self.current_state=="STARTING"):

            self.AC_power = 0 #FIXME: set to values
            self.AC_voltage = 0
            self.AC_current = 0


        elif(self.fault_status== "UNDER VOLTAGE" and self.current_state=="RUNNING"):
            self.AC_power = self.inverter.get_AC_output_power(self.DC_power)
            self.AC_voltage = self.inverter.set_AC_output_voltage(235 - random.randint(20,50)) #FIXME
            self.AC_current = self.inverter.get_AC_output_current()
        elif(self.fault_status=="GRID FAILURE" and self.AC_voltage>185):

            self.AC_current = self.inverter.get_AC_output_current()
        elif(self.fault_status=="GRID FAILURE" and self.AC_voltage<=185):
            self.DC_power = 0
            self.DC_current = 0

            self.AC_power = 0
            self.AC_voltage = 0
            self.AC_current = 0
            self.current_state = "OFF"
            self.state_machine.current_state = "OFF"


        else: #if off
            self.DC_power = 0
            self.DC_voltage = 0
            self.DC_current = 0

            self.AC_power = 0
            self.AC_voltage = 0
            self.AC_current = 0

        self.todays_energy = self.get_todays_energy()

        return {
            "timestamp": f"{int(self.timestamp//60):02d}:{int(self.timestamp%60):02d}",
            "dc_power": self.DC_power,
            "dc_voltage": self.DC_voltage,
            "dc_current": round(self.DC_current,4),
            "ac_power": round(self.AC_power,2),
            "ac_voltage": self.AC_voltage,
            "ac_current": round(self.AC_current,4),
            "todays_energy": round(self.todays_energy,2),
            "current_state": self.current_state,
            "condition_status": self.condition_status,
            "fault_status": self.fault_status
        }

    def get_todays_energy(self):
        self.todays_energy += 5/60 * self.AC_power
        return self.todays_energy
