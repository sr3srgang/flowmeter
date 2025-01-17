# Flow logging software for Sr3 use
- Created by Stella Kraus

## Functions
Periodically read flow in pipes and upload it to Sr group's Grafana's DB

## Set up
1. Install Kipling software for LabJack https://support.labjack.com/docs/kipling
2. Install Python for LJM https://support.labjack.com/docs/python-for-ljm-windows-mac-linux
3. Via USB, connect LabJack to a computer with Kipling downloaded 
4. Connect LabJack to Ethernet
5. Make appropriate analog connections between LabJack and flowmeters
6. In voltage_logger.py, update list << PINS = ["AIN0", "AIN2"] >> with pins that have analog connections on the LabJack
7. Update device = LabJackT7('192.168.1.92') with appropriate IP address for the LabJack
8. Since different flowmeters have different voltage to flow calibrations, in labjack_code.py update 
         if pin == "AIN0":
            flow = volts * 0.25 + 0.25
        elif pin == "AIN2":
            flow = volts * 0.15 + 0.25

    with correct calibrations for appropriate pins
9. run voltage_logger.py

