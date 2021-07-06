# Import libraries
import numpy as np
import os
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
# from PhysioNetData import medianFilter, bandStopFilter
from collections import deque
import csv

# Create object serial port

portName = "COM9"
baudRate = 9600
R = 30
Y_range = [-180, 180]
# ser = serial.Serial(portName, baudRate)
ser = serial.Serial(portName, int(baudRate), timeout=1, parity=serial.PARITY_NONE, stopbits=1)

### START QtApp #####
app = QtGui.QApplication([])            # initialize things
####################

win = pg.GraphicsWindow(title="Signal from Pitch and Roll")  # create a window
win.setBackground('w')
p = win.addPlot(title="Realtime Pitch and Roll plot")  # create empty space for the plot in the window
p.setYRange(min=int(Y_range[0]), max=int(Y_range[1]))
p.addLegend()

curve = p.plot(pen=pg.mkPen(color='k', width=2.0), name = "pitch") ##pitch curve
curve2 = p.plot(pen=pg.mkPen(color='b', width=2.0), name = "roll") ##roll curve



windowWidth = 100   # width of the window displaying the curve
pitch = linspace(0, 0, 100)   # create array that will contain the relevant time series
roll = linspace(0, 0, 100)   # create array that will contain the relevant time series
ptr = -windowWidth                       # set first x position
# Value = deque(maxlen=len(pitch))

# Realtime data plot.
# Each time this function is called, the data display is updated
def update():
    global curve, curve2, ptr, pitch, roll
    data = ser.readline().decode("utf-8")
    if len(data) > 1:
        data = str(data)
        data = data[4:-2]
        splitData = data.split(',')
        pitchStr = splitData[0]
        rollStr = splitData[1]
        pitch[:-1] = pitch[1:]  # shift pitch data in the temporal mean 1 sample left
        roll[:-1] = roll[1:]  # shift roll data in the temporal mean 1 sample left

        pitch[-1] = float(pitchStr[2:])   # vector containing the instantaneous values
        roll[-1] = float(rollStr[2:])   # vector containing the instantaneous values
        ptr += 1  # update x position for displaying the curve
        curve.setData(pitch)  # set the curve with these data
        curve2.setData(roll)  # set the curve with these data
        # curve.setPos(ptr, 0)  # set x posiYtion in the graph to 0
        QtGui.QApplication.processEvents()  # process the plot now
### MAIN PROGRAM ###
# this is a brutal infinite loop calling the realtime data plot
while True:
    update()

### END QtApp ###
pg.QtGui.QApplication.exec_() # you MUST put this at the end

##################

