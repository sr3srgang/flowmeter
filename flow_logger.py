import os
from time import sleep
from datetime import datetime
from labjack_flow import LabJackT7
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import traceback

# User parameters
LOG_DIR = "./logs/"
LOG_FILE = "voltage.log"
ERROR_FILE = "voltage_error.log"
INFLUX_URL = "http://yesnuffleupagus.colorado.edu:8086"
INFLUX_TOKEN = "yelabtoken"
INFLUX_ORG = "yelab"
INFLUX_BUCKET = "sr3"
MEASUREMENT = "FlowLogger"
LOG_INTERVAL = 15  # in seconds
PINS = ["AIN8", "AIN6", "AIN4"]

# Define calibration functions (user-specified)
CALIBRATION_FUNCTIONS = {
    "AIN8": lambda V: 3.8 * V ,  # Example: replace with your actual function
    "AIN6": lambda V: .2 * V ,
    "AIN4": lambda V: 2.8 * V,
}

# Define serial numbers for each pin
PIN_SERIALS = {
    "AIN8": "19102083730",
    "AIN6": "00291071",
    "AIN4": "02083729",
}

def main():
    # Initialize LabJack device
    device = LabJackT7('192.168.1.92')

    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    try:
        cycle = 0
        while True:
            try:
                cycle += 1
                print(f"Cycle {cycle}: Reading voltages...")

                for pin in PINS:
                    voltage = device.read_flow(pin)
                    flow = CALIBRATION_FUNCTIONS[pin](voltage)
                    serial = PIN_SERIALS[pin]
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    log_entry = f"{timestamp}, Pin: {pin}, Serial: {serial}, Voltage: {voltage:.4f} V, Flow: {flow:.4f}"
                    print(log_entry)

                    # Log to file
                    with open(os.path.join(LOG_DIR, LOG_FILE), "a") as f:
                        f.write(log_entry + "\n")

                    # Prepare InfluxDB record
                    record = [
                        {
                            "measurement": MEASUREMENT,
                            "tags": {
                                "Channel": pin,
                                "Serial": serial
                            },
                            "fields": {
                                "Raw Voltage (V)": voltage,
                                "Flow (calibrated)": flow
                            },
                            "time": datetime.utcnow().isoformat()
                        }
                    ]

                    # Upload to InfluxDB
                    with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
                        with client.write_api(write_options=SYNCHRONOUS) as writer:
                            writer.write(bucket=INFLUX_BUCKET, record=record)

            except Exception as e:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_message = f"{timestamp}, Error occurred: {str(e)}"
                with open(os.path.join(LOG_DIR, ERROR_FILE), "a") as f:
                    f.write(error_message + "\n")
                    f.write("".join(traceback.format_exception(None, e, e.__traceback__)) + "\n")

            sleep(LOG_INTERVAL)

    except KeyboardInterrupt:
        print("Logging stopped by user.")
    except Exception as e:
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
