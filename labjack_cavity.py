from labjack import ljm
import numpy as np

class LabJackT7:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def read_voltage(self, pin):
        handle = ljm.openS("T7", "ETHERNET", self.ip_address)
        voltage = ljm.eReadName(handle, pin)
        ljm.close(handle)  # Ensure the handle is properly closed after use
        return voltage

