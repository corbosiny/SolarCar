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
    self.commands = dict({
      "Get Input Voltage": "VoltageIn\n",
      "Get Output Voltage": "VoltageOut\n",
      "Get Input Current": "CurrentIn\n",
      "Get Output Current": "CurrentOut\n",
      "Get Input Power": "PowerIn\n",
      "Get Output Power": "PowerOut\n",
      "Get Duty Cycle": "DutyCycle\n"
    })
    self.varTrackers = dict({
      "Get Input Voltage": {
        'monitorActive': False,
        'time': [],
        'vals': []
      },
      "Get Output Voltage": {
        'monitorActive': False,
        'time': [],
        'vals': []
      },
      "Get Input Current": {
        'monitorActive': False,
        'time': [],
        'vals': []
      },
      "Get Output Current": {
        'monitorActive': False,
        'time': [],
        'vals': []
      },
      "Get Input Power": {
        'monitorActive': False,
        'time': [],
        'vals': []
      },
      "Get Output Power": {
        'monitorActive': False,
        'time': [],
        'vals': []
      },
      "Get Duty Cycle": {
        'monitorActive': False,
        'time': [],
        'vals': []
      }
    })
    self.time = []
    self.vals = []

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
    
    # Initialize window
    self.setGeometry(600, 600, 600, 440)
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
    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    self.monitorOutput.insertPlainText("[" + timestamp + "]\t" + response)
    sb = self.monitorOutput.verticalScrollBar()
    sb.setValue(sb.maximum())

    if "Voltage In" in response:
        self.time.append(timestamp)
        self.vals.append(int(re.sub('[^0-9]','', response)))

  def onClearButtonClicked(self):
    self.monitorOutput.clear()

  def sendAndReceive(self, text):
    if self.serialMonitor is None:
      self.appendDebugOutput("Error: No SerialMonitor instance\n")
      return

    # Convert text to board expected values
    if text in self.commands:
      command = self.commands[text]
      self.serialMonitor.sendStringToComPort(command)
      response = self.serialMonitor.getLineFromComPort()
      self.appendDebugOutput(response)
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
    plot.plot(self.time[-10:], self.vals[-10:])
    plot.gcf().autofmt_xdate()
    plot.show()

  '''
  Periodically request the power
  '''
  def periodicPoll(self, command, timeInterval):
    print(self.varTrackers[command])
    while (self.varTrackers[command]['monitorActive']):
      time.sleep(timeInterval)
      self.sendAndReceive(command)
    return
