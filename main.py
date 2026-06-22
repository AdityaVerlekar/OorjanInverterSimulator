

import csv
import os
import time
import threading

from simulator.telemetry import telemetry


def command_listener(sim, stop_event):
    print("\nInput ready")
    print("Available commands:")
    print("  fault GRID FAILURE")
    print("  fault OVER TEMPERATURE")
    print("  fault UNDER VOLTAGE")
    print("  fault COMMUNICATION LOSS")
    print("  condition LOW IRRADIANCE")
    print("  clear fault")
    print("  clear condition")
    print("  stop\n")

    while not stop_event.is_set():
        command = input("").strip().upper()

        if command == "STOP":
            stop_event.set()
            print("Stopping simulation...")

        elif command.startswith("FAULT "):
            fault_name = command.replace("FAULT ", "", 1)
            result = sim.fault_engine.set_fault(fault_name)
            print(result)

        elif command.startswith("CONDITION "):
            condition_name = command.replace("CONDITION ", "", 1)
            result = sim.fault_engine.set_condition(condition_name)
            print(result)

        elif command == "CLEAR FAULT":
            result = sim.fault_engine.clear_fault()
            print(result)

        elif command == "CLEAR CONDITION":
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



    start_hour = 7.5
    end_hour = 19
    sim_minute_real = 1     # if set to 0.5, 1 minute = 0.5 second

    total_minutes = int((end_hour - start_hour) * 60)

    print("Simulation started.")
    print(f"1 real second = {1/sim_minute_real:.3f} simulated minute(s)")
    print(f"Simulating from {int(start_hour)}:{round(start_hour%1*60):02d} AM to "
          f"{int(end_hour%12)}:{round(end_hour%1*60):02d} PM\n")

    listener_thread.start()

    try:
        for minute in range(total_minutes):
            if stop_event.is_set():
                break

            simulated_hour = start_hour + (minute / 60)
            simulated_minute = start_hour*60 + minute

            record = sim.collect_data(simulated_hour)
            records.append(record)

            display_hour = int(simulated_hour)
            display_minute = int((simulated_hour - display_hour) * 60)
            if(display_minute%5==0 or record['current_state'].strip()=='STARTING' or minute<6):
                print(
                    f"{display_hour:02d}:{display_minute:02d} | "
                    f"State: {record['current_state']} | "
                    f"DC: {round(record['dc_power'])} W | "
                    f"AC: {round(record['ac_power'])} W | "
                    f"Fault: {record['fault_status']} | "
                    f"Condition: {record['condition_status']}"
                )

            time.sleep(1/sim_minute_real)

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")

    finally:
        stop_event.set()
        save_to_csv(records, "sample_day_live.csv")
        print("Simulation ended.")


if __name__ == "__main__":
    run_simulation()