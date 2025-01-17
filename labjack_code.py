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

    def read_flow(self, pin):
        volts = self.read_voltage(pin)  # Pass pin to read_voltage
        print(f"Voltage read from {pin}: {volts:.4f}")
        
        if pin == "AIN0":
            flow = volts * 0.25 + 0.25
        elif pin == "AIN2":
            flow = volts * 0.15 + 0.25
        else:
            raise ValueError(f"Flow equation not defined for pin: {pin}")
        
        print(f"Calculated flow for {pin}: {flow:.4f}")
        return flow


# Example usage:
# out = LabJackT7("192.168.1.120").read_flow("AIN0")
# out = LabJackT7("192.168.1.120").read_flow("AIN2")



