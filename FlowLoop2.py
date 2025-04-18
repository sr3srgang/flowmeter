import numpy as np
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QDateTime
from PlotWindow import PlotWindow
import os

# libraries for data uploading
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

class FlowLoop(QWidget):
    def __init__(self, name, input_device, loop_time):
        super(FlowLoop, self).__init__()

        self.input_device = input_device
        self.loop_time = loop_time

        self.setWindowTitle(name)

        self.flow_label = QLabel("Current flow:")
        self.voltage_label = QLabel("V:")
        self.time_label = QLabel("Time")

        # Adding option to open pop-up plot
        self.plot_window = QPushButton(self)
        self.plot_window.setText('Show plot')
        self.plot_window.clicked.connect(self.make_window)
        self.plot_window.move(250, 1)

        layout = QGridLayout()
        layout.addWidget(self.time_label, 0, 0)
        layout.addWidget(self.voltage_label, 1, 0)
        layout.addWidget(self.flow_label, 1, 1)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(self.loop_time * 1000)

        # Setting up data log
        self.day = None
        self.f_path = None
        self.df_path = "C:/Users/srgang/Desktop/flowmeter/logs"  # Adjusted path to use absolute path
        self.f_name = "_flow_log.txt"

    def get_fname_write(self, dt):
        now = dt.toString('yyyy-MM-dd')
        if self.day != now:
            self.day = now
            folder_name = dt.toString('yyyyMMdd')
            folder_path = os.path.join(self.df_path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            this_file = folder_name + self.f_name
            self.f_path = os.path.join(folder_path, this_file)
            print(f"Generated file path: {self.f_path}")
        return self.f_path

    def make_window(self):
        fname_read = self.f_path
        if not fname_read or not os.path.exists(fname_read):
            print("Error: File path is invalid or does not exist.")
            return
        self.pw = PlotWindow(fname_read)
        self.pw.show()

    def update_loop(self):
        # Read temp, update window, log.
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.time_label.setText(timeDisplay)

        # Read in value from Keithley
        current_flow = self.input_device.read_flow()
        self.flow_label.setText("Current flow: {:.3f}".format(current_flow))

        # Log temp and output
        f_path = self.get_fname_write(time)

        # Send data to InfluxDB
        with InfluxDBClient(url="http://yesnuffleupagus.colorado.edu:8086", token="yelabtoken", org="yelab", debug=False) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write("data_logging", "yelab", "Sr3_flow,Channel=1 Value={}".format(current_flow))
            client.close()

        # Write data to file
        with open(f_path, 'a') as f:
            f.write("{}, {:.3f}\n".format(timeDisplay, current_flow))

        # Update voltage display
        self.voltage_label.setText("flow: {:.3f}".format(current_flow))
