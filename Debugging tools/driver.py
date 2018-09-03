#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication

from gui.serialMonitorViewer import SerialMonitorInterface
from serialMonitor.serialMonitor import SerialMonitor

if __name__ == "__main__":
  app = QApplication(sys.argv)
  serialMonitorInterface = SerialMonitorInterface()

  #comPort = "/dev/ttyACM0"
  #serialMonitor = SerialMonitor(comPort)
  #serialMonitorInterface.assignMonitor(serialMonitor)
  
  sys.exit(app.exec())
