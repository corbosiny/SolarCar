#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QGridLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QTextCursor

class SerialMonitorInterface(QWidget):
  
  def __init__(self):
    super().__init__()
    self.initUI()

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

  def onClearButtonClicked(self):
    self.monitorOutput.clear()

  '''
  On trigger of button pressed
  '''
  def onRequestButtonClicked(self):
    if self.serialMonitor is None:
      self.appendDebugOutput("Error: No SerialMonitor instance\n")
      return

    # Convert text to board expected values
    text = self.combobox.currentText()
    if text == "Get Input Voltage":
      command = "VoltageIn\n"
    elif text == "Get Output Voltage":
      command = "VoltageOut\n"
    elif text == "Get Input Current":
      command = "CurrentIn\n"
    elif text == "Get Output Current":
      command = "CurrentOut\n"
    elif text == "Get Input Power":
      command = "PowerIn\n"
    elif text == "Get Output Power":
      command = "PowerOut\n"
    elif text == "Get Duty Cycle":
      command = "DutyCycle\n"
    else:
      self.appendDebugOutput("Error: Unsupported option \"" + text + "\"\n")
      return
    
    # Ship request to board and print the response if possible
    self.serialMonitor.sendStringToComPort(command)
    response = self.serialMonitor.getLineFromComPort()
    self.appendDebugOutput(response)
