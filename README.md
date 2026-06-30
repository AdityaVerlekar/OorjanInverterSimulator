"# OorjanInverterSimulator" 

The Inverter Telemetry Simulator is created to help software developers to obtain, process and interact with the data from a simulated inverter rather than using actual data. 
The simulator, written in Python, uses FastAPI to mimic the real-world inverter API.
It can also be run without the API using the main.py code which runs in real time. 

The simulator generates the following data: DC voltage, DC current, DC power, AC voltage, AC current, AC power, Net energy generated for the day, Operation state, fault status and condition (low irradiance) status using a simulated daily irradiance curve.

The simulator has two modes: 
1. Progressive/live running where the speed of the simulation is 1 second = 5 simulated minutes by default. Faults and conditions must be preset before running this simulation. Live records with all data can be obtained for the instant. 
2. Instant day simulation where the day is simulated instantly. Faults and conditions must be preset and the simulation returns a json of the entire day's records. 


The faults that can be injected include grid failure and low voltage. In grid failure, the simulator emulates a Long Term Voltage Collapse: the AC voltage drops for up to 30 simulated minutes before it crosses the OFF threshold. In the low voltage fault scenario, the AC voltage drops and remains between the GRID FAILURE threshold and lower acceptable voltage threshold.
The faults can be inserted at any time in the progressive/live simulation as well as the instant day simulation. Grid failure takes precedence over low voltage in case of overlapping fault periods. 

The only condition present in the simulator, low irradiance, mimics a cloud or rainy day, reducing panel DC power output by 80%. Similar to the faults, it can be inserted at any time in both running modes.

Install dependencies using `pip install fastapi uvicorn pydantic`

In the terminal, run the API server `uvicorn api.server:app --reload`

In your browser, open API page `http://127.0.0.1:8000/docs`

To stop running the server, in the terminal, press Ctrl + C

##API Endpoints

`GET /`: Checks if the API is running.

`POST /simulate_day_instantly`: Runs the full simulation immediately and returns all records.

Example request:

```json
{
  "start_time": "05:00",
  "end_time": "20:00",
  "step_minutes": 5,
  "commands": [
    "li et1000",
    "fuv st1500",
    "fgf st1200 et1230"
  ]
}
```

### `POST /simulate_day_progressively`

Starts a real-time progressive simulation in the background.

### `GET /live_data`

Returns the latest telemetry record from the running progressive simulation.

### `GET /all_records_so_far`

Returns all records generated so far during the progressive simulation.

### `POST /stop`

Stops the currently running progressive simulation.

---

## Fault and Condition Commands

Supported commands:

```text
fgf = grid failure
fuv = under voltage
li  = low irradiance
```

Supported formats:

```text
fgf
fgf st0500
fgf et1400
fgf st0500 et1400
```

The same format works for `fuv` and `li`

Examples:

```text
li et1000          -> low irradiance until 10:00
fuv st1500         -> under voltage from 15:00 onward
fgf st1200 et1230  -> grid failure from 12:00 to 12:30
```

---

## Example Test Requests

Normal day:

```json
{
  "start_time": "05:00",
  "end_time": "20:00",
  "step_minutes": 5,
  "commands": []
}
```

Fault/condition scenario:

```json
{
  "start_time": "05:00",
  "end_time": "20:00",
  "step_minutes": 5,
  "commands": [
    "li et1000",
    "fuv st1500",
    "fgf st1200 et1230"
  ]
}
```
---




Note: This simulator is designed for software testing and development. It is not intended to be an electrically accurate inverter simulation.


