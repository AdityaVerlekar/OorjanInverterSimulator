

import csv
import os
import time
import threading

from simulator.telemetry import telemetry


def command_listener(sim, stop_event):
    print("\nInput ready")
    print("Available commands:")
    print("  fault GRID FAILURE / fgf") #Long Term Voltage Collapse which leads to GRID FAILURE
    print("  fault UNDER VOLTAGE / fuv")
    print("  condition LOW IRRADIANCE / li")
    print("  clear fault / cf")
    print("  clear condition / cc")
    print("  stop / s\n")

    while not stop_event.is_set():
        command = input("").strip().upper()

        if command == "STOP" or command == "S":
            stop_event.set()
            print("Stopping simulation...")

        elif command in ["FAULT GRID FAILURE", "FAULT UNDER VOLTAGE","FGF", "FUV"]:
            if(command.startswith("FAULT ")):
                fault_name = command.replace("FAULT ", "", 1)
            else:
                fault_name = "GRID FAILURE" if command[1:]=="GF" else "UNDER VOLTAGE"

            result = sim.fault_engine.set_fault(fault_name)
            print(result)

        elif command in ["CONDITION LOW IRRADIANCE", "LI"]:
            result = sim.fault_engine.set_condition("LOW IRRADIANCE")
            print(result)

        elif command in ["CLEAR FAULT","CF"]:
            result = sim.fault_engine.clear_fault()
            print(result)

        elif command in ["CLEAR CONDITION","CC"]:
            result = sim.fault_engine.clear_condition()
            print(result)

        else:
            print("Invalid command.")


def save_to_csv(records, filename):
    os.makedirs("data", exist_ok=True)

    filepath = os.path.join("data", filename)

    if len(records) == 0:
        print("No records to save.")
        return

    with open(filepath, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {filepath}")


def run_simulation():
    sim = telemetry()
    records = []

    stop_event = threading.Event()

    listener_thread = threading.Thread(
        target=command_listener,
        args=(sim, stop_event),
        daemon=True
    )



    start_hour = 9.5
    end_hour = 19
    sim_minute_real = 0.75     # Indicates how many minutes are processed per second
                            # if set to 0.5, 0.5 simulated minute = 1 real seconds
                            # if set to 4, 4 simulated minutes = 1 real seconds. 1 simulated minute = 1/4 seconds



    print("Solar Inverter Telemetry Simulator, Irradiance Data Based on Jaisalmer, RJ")
    print("\nSimulation started.")
    print(f"1 real second = {1/sim_minute_real:.3f} simulated minute(s)")
    print(f"Simulating from {int(start_hour)}:{round(start_hour%1*60):02d} AM to "
          f"{int(end_hour%12)}:{round(end_hour%1*60):02d} PM")

    listener_thread.start()
    time.sleep(0.5)

    try:
        i = 0
        for minute in range(int(start_hour*60), int(end_hour*60)+1,5):
            if stop_event.is_set():
                break

            simulated_hour = start_hour + (minute / 60)

            record = sim.collect_data(minute)
            records.append(record)


            print(
                f"{record['timestamp']} | "
                f"State: {record['current_state']} | "
                f"DC: {round(record['dc_power'])} W | "
                f"AC: {round(record['ac_power'])} W | "
                f"ACV: {record['ac_voltage']} | "
                f"Fault: {record['fault_status']} | "
                f"Condition: {record['condition_status']}"
            )

            i+=1
            time.sleep(1/sim_minute_real)

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")

    finally:
        stop_event.set()
        save_to_csv(records, "sample_day_live.csv")
        print("Simulation ended.")


if __name__ == "__main__":
    run_simulation()