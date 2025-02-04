from labjack import ljm
import numpy as np

class LabJackT7_cavity:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def read_voltage(self, pin):
        print(f"Attempting to read {pin} from LabJack...")
        handle = ljm.openS("T7", "ETHERNET", self.ip_address)
        print("Successfully opened LabJack handle.")
        voltage = ljm.eReadName(handle, pin)
        print(f"volts for {pin}: {voltage:.4f}")
        ljm.close(handle)  # Ensure the handle is properly closed after use
        return voltage

