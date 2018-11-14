#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import re
import matplotlib.pyplot as plot

from threading import Thread

from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QGridLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QTextCursor

class SerialMonitorInterface(QWidget):
  
  def __init__(self):
    super().__init__()
    self.initUI()
    self.monitorThreads = dict()
    self.outputMapping = dict({
      "Voltage In": "Get Input Voltage",
      "Voltage Out": "Get Output Voltage",
      "Current In": "Get Input Current",
      "Current Out": "Get Output Current",
      "Power In": "Get Input Power",
      "Power Out": "Get Output Power",
      "Duty Cycle": "Get Duty Cycle"
    })
    self.commands = dict({
      "Get Input Voltage": "VoltageIn\n",
      "Get Output Voltage": "VoltageOut\n",
      "Get Input Current": "CurrentIn\n",
      "Get Output Current": "CurrentOut\n",
      "Get Input Power": "PowerIn\n",
      "Get Output Power": "PowerOut\n",
      "Get Duty Cycle": "DutyCycle\n",

      "Current Algorithm": "CurrentAlgo\n",
      "Perturb and Observe": "PandO\n",
      "Incremental Conductance": "IncrementalConductance\n",
      "Fuzzy Logic": "FuzzyLogic\n"
    })
    self.varTrackers = dict({
      "Get Input Voltage": {
        'monitorActive': False,
        'time': [],
        'vals': [],
        'title': "Input Voltage",
        'y-label': "Voltage (V)"
      },
      "Get Output Voltage": {
        'monitorActive': False,
        'time': [],
        'vals': [],
        'title': "Output Voltage",
        'y-label': "Voltage (V)"
      },
      "Get Input Current": {
        'monitorActive': False,
        'time': [],
        'vals': [],
        'title': "Input Current",
        'y-label': "Current (A)"
      },
      "Get Output Current": {
        'monitorActive': False,
        'time': [],
        'vals': [],
        'title': "Output Current",
        'y-label': "Current (A)"
      },
      "Get Input Power": {
        'monitorActive': False,
        'time': [],
        'vals': [],
        'title': "Input Power",
        'y-label': "Power (W)"
      },
      "Get Output Power": {
        'monitorActive': False,
        'time': [],
        'vals': [],
        'title': "Ouput Power",
        'y-label': "Power (W)"
      },
      "Get Duty Cycle": {
        'monitorActive': False,
        'time': [],
        'vals': [],
        'title': "Duty Cycle",
        'y-label': "Percentage (%)"
      }
    })

  def assignMonitor(self, serialMonitor):
    self.serialMonitor = serialMonitor

  def initUI(self):
    # Initialize layout
    layout = QGridLayout()
    self.setLayout(layout)
    
    # Initialize Combobox
    self.combobox = QComboBox()
    self.combobox.addItem("Get Input Voltage")
    self.combobox.addItem("Get Output Voltage")
    self.combobox.addItem("Get Input Current")
    self.combobox.addItem("Get Output Current")
    self.combobox.addItem("Get Input Power")
    self.combobox.addItem("Get Output Power")
    self.combobox.addItem("Get Effective Power")
    self.combobox.addItem("Get Duty Cycle")

    self.combobox.currentTextChanged.connect(self.combobox_changed)
    layout.addWidget(self.combobox)

    # Initialize display text
    self.monitorOutput = QTextEdit()
    self.monitorOutput.setReadOnly(True)
    self.monitorOutput.setLineWrapMode(QTextEdit.NoWrap)
    font = self.monitorOutput.font()
    font.setFamily("Courier")
    font.setPointSize(10)
    layout.addWidget(self.monitorOutput)

    # Initialize request button
    requestButton = QPushButton("Interrogate board")
    requestButton.clicked.connect(self.onRequestButtonClicked)
    layout.addWidget(requestButton)

    # Initialize periodic poll button
    periodicPollButton = QPushButton("Periodically poll board")
    periodicPollButton.clicked.connect(self.onPeriodicPollButtonClicked)
    layout.addWidget(periodicPollButton)

    # Initialize stop monitoring button
    stopMonitorButton = QPushButton("Stop monitoring")
    stopMonitorButton.clicked.connect(self.onStopMonitorButtonClicked)
    layout.addWidget(stopMonitorButton)

    # Initialize plot button
    plotButton = QPushButton("Plot data")
    plotButton.clicked.connect(self.onPlotButtonClicked)
    layout.addWidget(plotButton)

    # Initialize clear button
    clearButton = QPushButton("Clear responses")
    clearButton.clicked.connect(self.onClearButtonClicked)
    layout.addWidget(clearButton)

    # Algo stuff here
    currAlgBtn = QPushButton("Current Algorithm")
    currAlgBtn.clicked.connect(self.onCurrAlgBtnClicked)
    layout.addWidget(currAlgBtn)

    self.algCombobox = QComboBox()
    self.algCombobox.addItem("Perturb and Observe")
    self.algCombobox.addItem("Incremental Conductance")
    self.algCombobox.addItem("Fuzzy Logic")
    layout.addWidget(self.algCombobox)

    switchAlgBtn = QPushButton("Switch Algorithm")
    switchAlgBtn.clicked.connect(self.onSwitchAlgBtnClicked)
    layout.addWidget(switchAlgBtn)


    
    # Initialize window
    self.setGeometry(900, 900, 600, 660)
    self.setWindowTitle("MPPT Debug Interface")
    self.show()

  '''
  On trigger of combobox change
  '''
  def combobox_changed(self):
    text = self.combobox.currentText()

  '''
  Append the response from the board to text display
  '''
  def appendDebugOutput(self, response):
    self.monitorOutput.moveCursor(QTextCursor.End)
    timestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    self.monitorOutput.insertPlainText("[" + timestamp + "]\t" + response.lstrip())
    sb = self.monitorOutput.verticalScrollBar()
    sb.setValue(sb.maximum())

    try:
      print(re.sub(r"\s*[^A-Za-z]+\s*", " ", response.lstrip())[:-3])
      outputMap = self.outputMapping[re.sub(r"\s*[^A-Za-z]+\s*", " ", response.lstrip())[:-3]]
      self.varTrackers[outputMap]['time'].append(timestamp)
      self.varTrackers[outputMap]['vals'].append(int(re.sub('[^0-9]','', response)))
    except:
      return

  def onClearButtonClicked(self):
    self.monitorOutput.clear()

  def sendDummy(self):
    self.sendAndReceive("Dummy\n")

  def sendAndReceive(self, text):
    if self.serialMonitor is None:
      self.appendDebugOutput("Error: No SerialMonitor instance\n")
      return

    # Convert text to board expected values
    if text in self.commands:
      command = self.commands[text]
      self.serialMonitor.sendStringToComPort(command)
      response = self.serialMonitor.getLineFromComPort()
      self.appendDebugOutput(response.rstrip("\n\r") + "\n")
      self.sendDummy()
    elif "Dummy" in text:
      self.serialMonitor.sendStringToComPort(text)
      response = self.serialMonitor.getLineFromComPort()
      return
    else:
      self.appendDebugOutput("Error: Unsupported option \"" + text + "\"\n")
      return

  '''
  On trigger of button pressed
  '''
  def onRequestButtonClicked(self):
    text = self.combobox.currentText()
    self.sendAndReceive(text)

  def onPeriodicPollButtonClicked(self):
    print("Poll pressed")
    text = self.combobox.currentText()
    self.varTrackers[text]['monitorActive'] = True
    Thread(
      target=self.periodicPoll,
      args=[text, 3]
    ).start()

  def onStopMonitorButtonClicked(self):
    text = self.combobox.currentText()
    self.varTrackers[text]['monitorActive'] = False

  def onPlotButtonClicked(self):
    text = self.combobox.currentText()
    plot.plot(
      self.varTrackers[text]['time'][-10:],
      self.varTrackers[text]['vals'][-10:]
    )
    plot.gcf().autofmt_xdate()
    plot.show()

  def onCurrAlgBtnClicked(self):
    self.sendAndReceive("Current Algorithm")

  def onSwitchAlgBtnClicked(self):
    text = self.algCombobox.currentText()
    self.sendAndReceive(text)

  '''
  Periodically request the power
  '''
  def periodicPoll(self, command, timeInterval):
    print(self.varTrackers[command])
    while (self.varTrackers[command]['monitorActive']):
      time.sleep(timeInterval)
      self.sendAndReceive(command)
    return