#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication
from threading import Thread

from gui.serialMonitorViewer import SerialMonitorInterface
from serialMonitor.serialMonitor import SerialMonitor

if __name__ == "__main__":
  app = QApplication(sys.argv)
  smi = SerialMonitorInterface()

  comPort = "/dev/ttyACM0"
  serialMonitor = SerialMonitor(comPort)
  smi.assignMonitor(serialMonitor)
  
  # Thread(target=smi.periodicPowerPoll).start()
  # smi.monitorThreads["VoltageIn\n"] = None
  sys.exit(app.exec())
