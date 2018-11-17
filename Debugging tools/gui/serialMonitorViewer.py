# -*- coding: utf-8 -*-

import datetime
import re
import time
from threading import Thread

import matplotlib.pyplot as plot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QPushButton,
                             QTextEdit, QWidget)

import gui.viewer_constants as vc
import gui.viewer_elements as ve


class SerialMonitorInterface(QWidget):
  
  def __init__(self):
    super().__init__()
    self.initUI()
    self.output_mapping  = vc.get_output_mapping()
    self.commands        = vc.get_command_mapping()
    self.var_trackers    = dict({
      vc.voltage_in['label']:  vc.get_var_tracker(vc.VOLTAGE_IN,  vc.voltage_in['unit']),
      vc.voltage_out['label']: vc.get_var_tracker(vc.VOLTAGE_OUT, vc.voltage_out['unit']),
      vc.current_in['label']:  vc.get_var_tracker(vc.CURRENT_IN,  vc.current_in['unit']),
      vc.current_out['label']: vc.get_var_tracker(vc.CURRENT_OUT, vc.current_out['unit']),
      vc.power_in['label']:    vc.get_var_tracker(vc.POWER_IN,    vc.power_in['unit']),
      vc.power_out['label']:   vc.get_var_tracker(vc.POWER_OUT,   vc.power_out['unit']),
      vc.duty_cycle['label']:  vc.get_var_tracker(vc.DUTY_CYCLE,  vc.duty_cycle['unit'])
    })

  def assignMonitor(self, serialMonitor):
    self.serial_monitor = serialMonitor

  def initUI(self):
    # Initialize layout
    layout = QGridLayout()
    self.setLayout(layout)
    
    # Initialize Combobox
    self.var_combo = ve.get_var_combobox()
    self.var_combo.currentTextChanged.connect(self.var_combo_changed)
    layout.addWidget(self.var_combo)

    # Initialize display text
    self.monitor_output = QTextEdit()
    self.monitor_output.setReadOnly(True)
    self.monitor_output.setLineWrapMode(QTextEdit.NoWrap)
    font = self.monitor_output.font()
    font.setFamily("Courier")
    font.setPointSize(10)
    layout.addWidget(self.monitor_output)

    # Initialize request button
    request_button = QPushButton("Interrogate board")
    request_button.clicked.connect(self.on_req_btn_clicked)
    layout.addWidget(request_button)

    # Initialize periodic poll button
    periodicPollButton = QPushButton("Monitor Board Value")
    periodicPollButton.clicked.connect(self.onPeriodicPollButtonClicked)
    layout.addWidget(periodicPollButton)

    # Initialize plot button
    plotButton = QPushButton("Plot data / Stop plotting")
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

    self.algo_combo = ve.get_alg_combobox()
    layout.addWidget(self.algo_combo)

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
  def var_combo_changed(self):
    text = self.var_combo.currentText()

  '''
  Append the response from the board to text display
  '''
  def appendDebugOutput(self, response):
    self.monitor_output.moveCursor(QTextCursor.End)
    timestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    self.monitor_output.insertPlainText("[" + timestamp + "]\t" + response.lstrip())
    sb = self.monitor_output.verticalScrollBar()
    sb.setValue(sb.maximum())

    try:
      outputMap = self.output_mapping[re.sub(r"\s*[^A-Za-z]+\s*", " ", response.lstrip())[:-3]]
      self.var_trackers[outputMap]['time'].append(timestamp)
      self.var_trackers[outputMap]['vals'].append(int(re.sub('[^0-9]','', response)))
    except:
      return

  def onClearButtonClicked(self):
    self.monitor_output.clear()

  def sendDummy(self):
    self.sendAndReceive("Dummy\n")

  def sendAndReceive(self, text):
    if self.serial_monitor is None:
      self.appendDebugOutput("Error: No SerialMonitor instance\n")
      return

    # Convert text to board expected values
    if text in self.commands:
      command = self.commands[text]
      self.serial_monitor.sendStringToComPort(command)
      response = self.serial_monitor.getLineFromComPort()
      self.appendDebugOutput(response.rstrip("\n\r") + "\n")
      self.sendDummy()
    elif "Dummy" in text:
      self.serial_monitor.sendStringToComPort(text)
      response = self.serial_monitor.getLineFromComPort()
      return
    else:
      self.appendDebugOutput("Error: Unsupported option \"" + text + "\"\n")
      return

  '''
  On trigger of button pressed
  '''
  def on_req_btn_clicked(self):
    text = self.var_combo.currentText()
    self.sendAndReceive(text)

  def onPeriodicPollButtonClicked(self):
    text = self.var_combo.currentText()
    if not self.var_trackers[text]['monitorActive']:
      text = self.var_combo.currentText()
      Thread(
          target=self.periodicPoll,
          args=[text, 3]
      ).start()

    self.var_trackers[text]['monitorActive'] = not self.var_trackers[text]['monitorActive'] 

  def onCurrAlgBtnClicked(self):
    self.sendAndReceive("Current Algorithm")

  def onSwitchAlgBtnClicked(self):
    text = self.algo_combo.currentText()
    self.sendAndReceive(text)

  def plotData(self, data):
    plot.figure(self.var_trackers[data]['title'])
    plot.ion()
    plot.show(block=False)

    while self.var_trackers[data]['plotActive']:
      plot.cla()
      plot.title(self.var_trackers[data]['title'])
      plot.xlabel("Time (s)")
      plot.ylabel(self.var_trackers[data]['y-label'])
      plot.plot(
        self.var_trackers[data]['time'][-10:],
        self.var_trackers[data]['vals'][-10:]
      )
      plot.gcf().autofmt_xdate()
      plot.draw()
      plot.pause(0.001)

  def onPlotButtonClicked(self):
    text = self.var_combo.currentText()

    if not self.var_trackers[text]['plotActive']:
      self.var_trackers[text]['plotActive'] = True
      Thread(
        target=self.plotData,
        args=[text]
      ).start()
    else:
      self.var_trackers[text]['plotActive'] = False

  '''
  Periodically request the power
  '''
  def periodicPoll(self, command, timeInterval):
    while (self.var_trackers[command]['monitorActive']):
      time.sleep(timeInterval)
      self.sendAndReceive(command)
    return