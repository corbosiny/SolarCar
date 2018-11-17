#!/usr/bin/env python

import re
import sys
from threading import Lock

import serial


class SerialMonitor():

  def __init__(self, comPort, baudRate = 115200):
    self.comPort = comPort
    self.baudRate = baudRate
    self.serialConnection = serial.Serial(comPort, baudRate)
    self.outboundLock = Lock()
    self.inboundLock = Lock()

  def displaySerialMonitor(self):
    if self.dataIsAvailable:
      serialMonitorData = self.getLineFromComPort()
      print(serialMonitorData, end= '')
      
  def getIntFromComPort(self):
    serialData = self.getLineFromComPort()
    return int(serialData)

  def getFloatFromComPort(self):
    serialData = self.getLineFromComPort()
    floatVal = re.compile(r'[^\d.]+')
    return float(floatVal.sub('', serialData))

  def getLineFromComPort(self):
    self.inboundLock.acquire()
    line = ''
    lastCharReceived = ''
    while '\n' not in lastCharReceived:
      lastCharReceived = self.getCharFromComPort()
      line += lastCharReceived
    self.inboundLock.release()

    return line

  def getCharFromComPort(self):
    try:
      return self.getByteFromComPort().decode("utf-8")
    except:
      return ""
      
  def getByteFromComPort(self):
    return self.serialConnection.read()

  def dataIsAvailable():
    if self.serialConnection.in_waiting > 0:
      return True

  def sendNumToComPort(self, numToSend):
    numAsString = str(numToSend)
    self.sendStringToComPort(numAsString)

  def sendStringToComPort(self, message):
    self.outboundLock.acquire()
    self.sendBytesToComPort(message.encode('utf-8'))
    self.outboundLock.release()

  def sendBytesToComPort(self, bytesToSend):
    self.serialConnection.write(bytesToSend)

if __name__ == "__main__":
  comPort = "/dev/ttyACM0"
  newMonitor = SerialMonitor(comPort)
  while True:
    userInput = input(">>")
    newMonitor.sendStringToComPort(userInput + "\n")
    newMonitor.displaySerialMonitor()
