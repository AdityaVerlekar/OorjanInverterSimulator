class fault_engine:
    def __init__(self):

        #Environmental Inputs
        self.irradiance = 0 #TODO
        #Fixme: do we need this? self.plant_capacity = 0

        self.NO_FAULT = "NO FAULT"
        self.GRID_FAILURE = "GRID FAILURE"
        self.UNDER_VOLTAGE = "UNDER VOLTAGE"
        self.fault_status = "NO FAULT"

        self.LOW_IRRADIANCE = "LOW IRRADIANCE"
        self.NO_CONDITION = "NO CONDITION"
        self.condition_status = "NO CONDITION"


    def check_fault_status(self):
        return self.fault_status

    def check_condition_status(self):
        return self.condition_status

    def set_fault(self, fault):
        if fault.strip() not in ["GRID FAILURE", "UNDER VOLTAGE"]:
            return "INVALID FAULT, current status: "+self.fault_status+"\n"
        fault = fault.strip()

        if(fault == "UNDER VOLTAGE" and self.fault_status=="GRID FAILURE"):
            return "UNSUCESSFUL, current fault status: "+self.fault_status+"; clear GRID FAILURE first"
        elif(fault == "UNDER VOLTAGE"):
            self.fault_status = fault
            return "SUCCESS, current fault status: " + self.fault_status
        #else:
        self.fault_status = "GRID FAILURE"
        return f"SUCCESS, current fault status: UNDER VOLTAGE; {self.fault_status} imminent\n"


    def set_condition(self, condition):
        if(condition.strip() != "LOW IRRADIANCE"):
            return "INVALID CONDITION, current status: " + self.condition_status+"\n"
        self.condition_status = condition.strip()
        return "SUCCESS, current condition status: " + self.condition_status+"\n"


    def clear_fault(self):
        self.fault_status = self.NO_FAULT
        return "SUCCESS, current fault status: " + self.fault_status+"\n"

    def clear_condition(self):
        self.condition_status = self.NO_CONDITION
        return "SUCCESS, current condition status: " + self.condition_status+"\n"




