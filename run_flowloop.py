import numpy as np
from FlowLoop import FlowLoop
import sys
from PyQt5.QtWidgets import QApplication
from labjack_code import abjack_code


if __name__ == '__main__':
    app = QApplication(sys.argv)
    l = labjack_code('192.168.1.120')
    loop=TempLoop("Flow", l, 10)
    loop.show()
    sys.exit(app.exec_())