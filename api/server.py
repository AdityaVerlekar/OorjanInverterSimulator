from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from simulator.telemetry import telemetry


app = FastAPI(title="Inverter Telemetry Simulator API")


class FaultInput(BaseModel):
    type: str
    start_time: str
    end_time: str


class SimulationRequest(BaseModel):
    start_time: str = "05:00"
    end_time: str = "20:00"
    step_minutes: int = 5
    faults: List[FaultInput] = []


def time_to_minutes(time_string):
    try:
        hour, minute = time_string.split(":")
        return int(hour) * 60 + int(minute)
    except:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid time format: {time_string}. Use HH:MM format."
        )


def convert_fault_name(api_fault_name):
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


def get_active_fault(current_minute, faults):
    for fault in faults:
        fault_start = time_to_minutes(fault.start_time)
        fault_end = time_to_minutes(fault.end_time)

        if fault_start <= current_minute <= fault_end:
            return convert_fault_name(fault.type)

    return "NO FAULT"


@app.get("/")
def root():
    return {
        "message": "Inverter Telemetry Simulator API is running"
    }


@app.post("/simulate")
def simulate(request: SimulationRequest):
    sim = telemetry()
    records = []

    start_minute = time_to_minutes(request.start_time)
    end_minute = time_to_minutes(request.end_time)

    if end_minute <= start_minute:
        raise HTTPException(
            status_code=400,
            detail="end_time must be after start_time"
        )

    if request.step_minutes <= 0:
        raise HTTPException(
            status_code=400,
            detail="step_minutes must be greater than 0"
        )

    for minute in range(start_minute, end_minute + 1, request.step_minutes):
        active_fault = get_active_fault(minute, request.faults)

        if active_fault == "NO FAULT":
            sim.fault_engine.clear_fault()
        else:
            sim.fault_engine.set_fault(active_fault)

        record = sim.collect_data(minute)
        records.append(record)

    return {
        "start_time": request.start_time,
        "end_time": request.end_time,
        "step_minutes": request.step_minutes,
        "record_count": len(records),
        "records": records
    }