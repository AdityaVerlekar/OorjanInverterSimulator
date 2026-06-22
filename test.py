import csv
import os
import threading
from simulator.telemetry import telemetry

def command_listener(sim, stop_event):
    print("Command listener started.")
    print("Commands:")
    print("  fault GRID FAILURE")
    print("  fault OVER TEMPERATURE")
    print("  fault UNDER VOLTAGE")
    print("  fault COMMUNICATION LOSS")
    print("  condition LOW IRRADIANCE")
    print("  clear fault")
    print("  clear condition")
    print("  stop")

    while not stop_event.is_set():
        command = input("> ").strip().upper()

        if command == "STOP":
            stop_event.set()

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


def minute_to_hour(minute):
    return minute / 60


def run_daily_simulation():
    sim = telemetry()
    telemetry_records = []

    for minute in range(0, 24 * 60):
        hour_timestamp = minute_to_hour(minute)

        data = sim.collect_data(hour_timestamp)
        telemetry_records.append(data)

    return telemetry_records


def save_to_csv(records, filename):
    os.makedirs("data", exist_ok=True)

    filepath = os.path.join("data", filename)

    with open(filepath, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())

        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {filepath}")


def main():
    records = run_daily_simulation()

    save_to_csv(records, "sample_day.csv")

    # Print a few sample records for checking
    for record in records[::60]:
        print(record)


if __name__ == "__main__":
    main()