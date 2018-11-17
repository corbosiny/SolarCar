import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from flask import Flask
from gui.serialMonitorViewer import SerialMonitorInterface
from serialMonitor.serialMonitor import SerialMonitor

smv_app = None
flask_app = Flask(__name__)
@flask_app.route('/')
def index():
  return smv_app.commands['Get Input Voltage']

class FlaskThread(QThread):
  def __init__(self, application):
    QThread.__init__(self)
    self.application = application

  def __del__(self):
    self.wait()

  def run(self):
    self.application.run(debug=False)

def init_gui(serialMonitor):
  # Initialize QtApp and Flask app
  app = QApplication(sys.argv)
  webapp = FlaskThread(flask_app)
  webapp.start()

  # Assign the serialMonitor library
  global smv_app
  smv_app = SerialMonitorInterface()
  smv_app.assignMonitor(serialMonitor)
  return app.exec()

def main():
  comPort = "/dev/ttyACM0"
  serialMonitor = SerialMonitor(comPort)
  sys.exit(init_gui(serialMonitor))

if __name__ == "__main__":
  main()