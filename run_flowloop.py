import numpy as np
from FlowLoop2 import FlowLoop
import sys
from PyQt5.QtWidgets import QApplication
from labjack_code import LabJackT7


if __name__ == '__main__':
    app = QApplication(sys.argv)
    l = LabJackT7('192.168.1.92')
    loop=FlowLoop("Flow", l, 5)
    loop.show()
    sys.exit(app.exec_())