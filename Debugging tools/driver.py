#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication
from threading import Thread
import multiprocessing

from gui.serialMonitorViewer import SerialMonitorInterface
from serialMonitor.serialMonitor import SerialMonitor

def start_gui(serialMonitor):
  app = QApplication(sys.argv)
  smi = SerialMonitorInterface()
  smi.assignMonitor(serialMonitor)
  sys.exit(app.exec())

if __name__ == "__main__":
  app = QApplication(sys.argv)
  comPort = "/dev/ttyACM0"
  serialMonitor = SerialMonitor(comPort)

  start_gui(serialMonitor)