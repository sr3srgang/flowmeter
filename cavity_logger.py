import os
from time import sleep
from datetime import datetime
from labjack_cavity import LabJackT7_cavity
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import traceback

# User parameters
LOG_DIR = "./logs/"
LOG_FILE = "cavity_voltage.log"
ERROR_FILE = "cavity_voltage_error.log"
INFLUX_URL = "http://yesnuffleupagus.colorado.edu:8086"
INFLUX_TOKEN = "yelabtoken"
INFLUX_ORG = "yelab"
INFLUX_BUCKET = "sr3"
MEASUREMENT = "cavity_VoltageLogger"
TAG = "Channel"
FIELD = "Voltage at"
LOG_INTERVAL = 15  # in seconds
PINS = ["AIN0"]  # List of pins to read

def main():
    # Initialize LabJack device
    device = LabJackT7_cavity('192.168.1.92')

    # Ensure log directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    try:
        cycle = 0  # Keeps track of logging cycles
        while True:
            try:
                cycle += 1
                print(f"Cycle {cycle}: Reading voltages...")

                # Iterate over pins and read flow
                for pin in PINS:
                    print(f"Reading from pin: {pin}")
                    voltage = device.read_voltage(pin)

                    # Log voltage data
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"{timestamp}, Pin: {pin}, Voltage: {voltage:.4f} V"
                    print(f"Cycle {cycle}: {log_entry}")

                    with open(os.path.join(LOG_DIR, LOG_FILE), "a") as f:
                        f.write(log_entry + "\n")

                    # Format data for InfluxDB
                    record = [
                        {
                            "measurement": MEASUREMENT,
                            "tags": {TAG: pin},
                            "fields": {FIELD: voltage},
                            "time": datetime.utcnow().isoformat()
                        }
                    ]

                    # Upload to InfluxDB
                    #print(f"Cycle {cycle}: Uploading data for {pin} to InfluxDB...")
                    with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
                        with client.write_api(write_options=SYNCHRONOUS) as writer:
                            writer.write(bucket=INFLUX_BUCKET, record=record)

                #print(f"Cycle {cycle}: Upload successful for all pins. Waiting for the next cycle...")

            except Exception as e:
                # Log the error
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_message = f"{timestamp}, Error occurred: {str(e)}"
                #print(f"Cycle {cycle}: {error_message}")
                with open(os.path.join(LOG_DIR, ERROR_FILE), "a") as f:
                    f.write(error_message + "\n")
                    f.write("".join(traceback.format_exception(None, e, e.__traceback__)) + "\n")

            # Wait until next interval
            sleep(LOG_INTERVAL)

    except KeyboardInterrupt:
        print("Logging stopped by user.")
    except Exception as e:
        # Catch and log any unexpected errors
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        critical_error = f"{timestamp}, Critical Error: {str(e)}"
        print(critical_error)
        with open(os.path.join(LOG_DIR, ERROR_FILE), "a") as f:
            f.write(critical_error + "\n")
            f.write("".join(traceback.format_exception(None, e, e.__traceback__)) + "\n")
    finally:
        print("Voltage logger terminated.")


if __name__ == "__main__":
    main()
