class fault_engine:
    def __init__(self):

        #Environmental Inputs
        self.irradiance = 0 #TODO: is this necessary
        self.temperature = 0 #TODO: how do I get this
        self.plant_capacity = 0 #TODO: what does this mean?

        self.NO_FAULT = "NO FAULT"
        self.GRID_FAILURE = "GRID FAILURE"
        self.OVER_TEMPERATURE = "OVER TEMPERATURE"
        self.UNDER_VOLTAGE = "UNDER VOLTAGE"
        self.COMMUNICATION_LOSS = "COMMUNICATION LOSS"
        self.fault_status = "NO FAULT"

        self.LOW_IRRADIANCE = "LOW IRRADIANCE"
        self.NO_CONDITION = "NO CONDITION"
        self.condition_status = "NO CONDITION"


    def check_fault_status(self):
        return self.fault_status

    def check_condition_status(self):
        return self.condition_status

    def set_fault(self, fault):
        if fault.strip() not in ["NO FAULT", "GRID FAILURE", "OVER TEMPERATURE", "UNDER VOLTAGE", "COMMUNICATION LOSS"]:
            return "INVALID FAULT, current status: "+self.fault_status
        self.fault_status = fault.strip()
        return "SUCCESS, current fault status: "+self.fault_status

    def set_condition(self, condition):
        if condition.strip() not in ["NO CONDITION", "LOW IRRADIANCE"]:
            return "INVALID CONDITION, current status: " + self.condition_status
        self.condition_status = condition.strip()
        return "SUCCESS, current condition status: " + self.condition_status

    def clear_fault(self):
        self.fault_status = self.NO_FAULT
        return "SUCCESS, current fault status: " + self.fault_status

    def clear_condition(self):
        self.condition_status = self.NO_CONDITION
        return "SUCCESS, current condition status: " + self.condition_status




