from fastapi import FastAPI, HTTPException #http exception is for error response
from pydantic import BaseModel #validates json input
from typing import List #helps create a list of type: Object

from simulator.telemetry import telemetry


app = FastAPI(title="Inverter Telemetry Simulator API") #create the "app" that the Uvicorn server will run


class FaultCondInput(BaseModel): #structure of fault input
    type: str
    start_time: str
    end_time: str


class SimulationRequest(BaseModel): #simulate request format
    start_time: str = "05:00"
    end_time: str = "20:00"
    step_minutes: int = 5
    faults: List[FaultCondInput] = [] #you can insert multiple faults
    conditions: List[FaultCondInput] = []
    commands: List[str] = []


def time_to_minutes(time_string):
    try:
        hour, minute = time_string.split(":")
        if(0<=int(hour)<24 and 0<=int(minute)<=59):
            return int(hour)*60 + int(minute)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid time- {time_string}"
            )
    except:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid time- {time_string}"
        )


def convert_fault_name(api_fault_name): #converts the nospace fault names used in APInames into the names used in my function
    fault_map = {
        "grid-failure": "GRID FAILURE",
        "under-voltage": "UNDER VOLTAGE",
        "no-fault": "NO FAULT"
    }

    if api_fault_name not in fault_map:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid fault type: {api_fault_name}"
        )

    return fault_map[api_fault_name]

def convert_condition_name(api_condition_name):
    condition_map= {
        "low-irradiance": "LOW IRRADIANCE",
        "no-condition": "NO CONDITION",
    }

    if api_condition_name not in condition_map:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid condition type: {api_condition_name}"
        )

    return condition_map[api_condition_name]

#fgf - runs throughout - 0000-2359
#fgf st0500 - starts at 0500, continues to end of sim
#fgf et1400 - begins at simulation start, ends at 1400
#fgf st0500 et1400 - begins at 0500, ends at 1400

def raise_invalid_command():
    raise HTTPException(
        status_code=400,
        detail=f"Invalid command"
    )

def parse_command(command):
    command = command.split()
    command = [item.lower() for item in command]

    if(len(command)>3 or len(command)<1):
        raise_invalid_command()
    if(command[0] not in ["fgf", "fuv", "li"]):
        raise_invalid_command()
    if(len(command)==2):
        if(command[1][0:2] not in ["st", "et"]):
            raise_invalid_command()
        if(len(command[1][2:])!=4 or not command[1][2:].isdigit()):
            raise_invalid_command()
    if(len(command)==3):
        if (command[1][0:2] !="st" or command[2][0:2] !="et"):
            raise_invalid_command()
        if (len(command[1][2:]) != 4 or not command[1][2:].isdigit() or len(command[2][2:]) != 4 or not command[2][2:].isdigit()):
            raise_invalid_command()

    faultcond = command[0]
    if(len(command)==1):
        st = "00:00"
        et = "23:59"
    elif(len(command)==2):
        st = command[1][2:4]+":"+command[1][4:] if command[1][0:2] == "st" else "-1"
        et = command[1][2:4]+":"+command[1][4:] if st=="-1" else "23:59"
        st = "00:00" if st=="-1" else st
    else:
        st = command[1][2:4]+":"+command[1][4:]
        et = command[2][2:4]+":"+command[2][4:]

    if time_to_minutes(et) < time_to_minutes(st):
        raise_invalid_command()

    command_map = {
        "fgf": {
            "category": "fault",
            "type": "grid-failure"
        },
        "fuv": {
            "category": "fault",
            "type": "under-voltage"
        },
        "li": {
            "category": "condition",
            "type": "low-irradiance"
        }
    }

    return {
        "category": command_map[faultcond]["category"],
        "type": command_map[faultcond]["type"],
        "start_time": st,
        "end_time": et
    }





def get_active_fault(current_minute, faults): #implements fault at the minute if scheduled
    active_faults = []
    for fault in faults:
        fault_start = time_to_minutes(fault.start_time)
        fault_end = time_to_minutes(fault.end_time)

        if fault_start <= current_minute <= fault_end:
            active_faults.append( convert_fault_name(fault.type))
    if("GRID FAILURE" in active_faults):
        return "GRID FAILURE"
    if("UNDER VOLTAGE" in active_faults):
        return "UNDER VOLTAGE"

    return "NO FAULT"

def get_active_condition(current_minute, conditions): #implements fault at the minute if scheduled
    for condition in conditions:
        cond_start = time_to_minutes(condition.start_time)
        cond_end = time_to_minutes(condition.end_time)

        if cond_start <= current_minute < cond_end:
            return convert_condition_name(condition.type)

    return "NO CONDITION"


@app.get("/") #when someone sends "GET /" request , root is run
def root():
    return {
        "message": "Inverter Telemetry Simulator API is running"
    }


@app.post("/simulate")  #when someone sends POST /SIMULATE
def simulate(request: SimulationRequest): #request should follow format of SimulationRequest
    sim = telemetry()
    records = []



    start_minute = time_to_minutes(request.start_time)
    end_minute = time_to_minutes(request.end_time)

    if end_minute <= start_minute:
        raise HTTPException(
            status_code=400,
            detail="end_time must be after start_time"
        )
    elif start_minute <0 or end_minute>24*60:
        raise HTTPException(
            status_code=400,
            detail="time outside 0-24 hour range"
        )

    if request.step_minutes <= 0:
        raise HTTPException(
            status_code=400,
            detail="step_minutes must be greater than 0"
        )


    all_faults = list(request.faults)
    all_conditions = list(request.conditions)

    for command in request.commands:
        parse = parse_command(command)
        new_input = FaultCondInput(
            type= parse["type"],
            start_time= parse["start_time"],
            end_time= parse["end_time"]
        )
        if(parse["category"]=="fault"):
            all_faults.append(new_input)
        elif(parse["category"]=="condition"):
            all_conditions.append(new_input)


    for minute in range(start_minute, end_minute + 1, request.step_minutes):
        active_fault = get_active_fault(minute, all_faults)
        active_condition = get_active_condition(minute, all_conditions)


        sim.fault_engine.clear_fault()

        if active_fault != "NO FAULT":
            sim.fault_engine.set_fault(active_fault)

        if(active_condition == "NO CONDITION"):
            sim.fault_engine.clear_condition()
        else:
            sim.fault_engine.set_condition(active_condition)

        record = sim.collect_data(minute)
        records.append(record)

    return {
        "start_time": request.start_time,
        "end_time": request.end_time,
        "step_minutes": request.step_minutes,
        "record_count": len(records),
        "records": records
    }