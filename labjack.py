from labjack import ljm

class LabJackT7:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def read_voltage_AIN0(self):
        handle = ljm.openS("T7", "ETHERNET", self.ip_address)
        voltage = ljm.eReadName(handle, "AIN0")
        print(f"Voltage at AIN0: {voltage:.4f} V")
        return voltage

    def read_flow(self):
        resistance = self.read_resistance()
        local_slope = 1/(-1.7e+3) #1 degree per 1.7 kOhm in neighborhood of 22C, 33 kOhm
        temp = (resistance-40.77e+3)*local_slope + 18 #44008RC thermistor
        return temp, resistance
out = LabJackT7("192.168.1.120").read_voltage_AIN0()

