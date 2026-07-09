class inverter_model:
    def __init__(self):
        self.efficiency = 0.98

        self.AC_voltage = 232 #India electricty main voltage +2 from inverter so current can flow

        self.AC_power = 0
        self.AC_current = 0

    def get_AC_output_power(self, panel_DC_power):
        self.AC_power = panel_DC_power*self.efficiency
        return self.AC_power

    def get_AC_output_voltage(self):
        return self.AC_voltage

    def set_AC_output_voltage(self, new_voltage):
        self.AC_voltage = new_voltage
        return self.AC_voltage

    def get_AC_output_current(self):
        self.AC_current = self.AC_power/self.AC_voltage
        return self.AC_current
