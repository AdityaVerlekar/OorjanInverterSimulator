# Oorjan Inverter Simulator

The Inverter Telemetry Simulator is created to help software developers obtain, process and interact with telemetry data from a simulated inverter rather than a physical inverter.
The simulator, written in Python, uses FastAPI to mimic the real-world inverter API.
It can also be run without the API using the `main.py` code which runs in real time.

The simulator generates the following data:
- DC voltage
- DC current
- DC power
- AC voltage
- AC current
- AC power
- Cumulative daily energy
- Operation state
- Fault status
- Condition (low irradiance) status

The simulator has two modes:
1. Progressive/live running where the speed of the simulation is **1 second = 5 simulated minutes** by default. Faults and conditions must be preset before running this simulation. Live records with all data can be obtained at any instant.
2. Instant day simulation where the day is simulated instantly. Faults and conditions must be preset and the simulation returns a JSON containing the entire day's records.

The faults that can be injected include **grid failure** and **under-voltage**. In grid failure, the simulator emulates a Long Term Voltage Collapse: the AC voltage drops for up to 30 simulated minutes before it crosses the OFF threshold. In the under-voltage fault scenario, the AC voltage drops and remains between the GRID FAILURE threshold and lower acceptable voltage threshold.

Faults can be scheduled at any time in both the progressive/live simulation and the instant day simulation. Grid failure takes precedence over under-voltage in the case of overlapping fault periods.

The only condition present in the simulator, **low irradiance**, mimics a cloudy or rainy day by reducing panel DC power output by 80%. Similar to the faults, it can be inserted at the beginning for any time in both running modes.

---

## Installation

Create a virtual environment.

**Windows**

```text
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```text
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies.

```text
pip install -r requirements.txt
```

Run the API server.

```text
uvicorn api.server:app --reload
```

Open the API documentation.

```text
http://127.0.0.1:8000/docs
```

To stop the running server, press **Ctrl + C** in the terminal.

---

## Project Structure

```text
api/                FastAPI server
simulator/          Core simulator modules
main.py             Real-time simulator
requirements.txt    Python dependencies
README.md
```

---

## API Endpoints

`GET /`

Checks if the API is running.

---

`POST /simulate_day_instantly`

Runs the full simulation immediately and returns all records.

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

---

`POST /simulate_day_progressively`

Starts a real-time progressive simulation in the background.

---

`GET /live_data`

Returns the latest telemetry record from the running progressive simulation.

---

`GET /all_records_so_far`

Returns all records generated so far during the progressive simulation.

---

`POST /stop`

Stops the currently running progressive simulation.

---

## Fault and Condition Commands

Supported commands:

```text
fgf = grid failure
fuv = under voltage
li  = low irradiance
```

Supported format examples:

```text
fgf
fgf st0500
fgf et1400
fgf st0500 et1400
```

The same format works for `fuv` and `li`.

More examples:

```text
li et1000          -> low irradiance from simulation start until 10:00
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

Example response (partial):

```json
{
  "timestamp": "09:00",
  "dc_power": 326,
  "ac_power": 313,
  "ac_voltage": 233,
  "current_state": "RUNNING",
  "fault_status": "NO FAULT",
  "condition_status": "NO CONDITION"
}
```

---

## Limitations

This simulator is designed for software testing and development. It is **not** intended to be an electrically accurate inverter simulation.

The simulator uses a simplified irradiance and power model and does not model MPPT behaviour, inverter harmonics, grid synchronization or detailed thermal dynamics.