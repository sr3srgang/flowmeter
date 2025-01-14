from labjack import ljm
import numpy as np

class LabJackT7:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def read_voltage_AIN0(self):
        handle = ljm.openS("T7", "ETHERNET", self.ip_address)
        voltage = ljm.eReadName(handle, "AIN0")
        print(f"Voltage at AIN0: {voltage:.4f} V")
        return voltage

#out = LabJackT7("192.168.1.120").read_voltage_AIN0()

