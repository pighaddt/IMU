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

portName = "COM4"
baudRate = 115200    # FW1.0 115200 FW2.0 9600
R = 30
Y_range = [-180, 180]
# ser = serial.Serial(portName, baudRate)
ser = serial.Serial(portName, int(baudRate), timeout=1, parity=serial.PARITY_NONE, stopbits=1)

### START QtApp #####
app = QtGui.QApplication([])            # initialize things
####################

win = pg.GraphicsWindow(title="Signal from IMU Vx and Vy and Vz")  # create a window
win.setBackground('w')
p = win.addPlot(title="Realtime IMU Vx  Vy Vz")  # create empty space for the plot in the window
p.setYRange(min=int(Y_range[0]), max=int(Y_range[1]))
p.addLegend()

curve = p.plot(pen=pg.mkPen(color='k', width=2.0), name = "Vx") ##pitch curve
curve2 = p.plot(pen=pg.mkPen(color='b', width=2.0), name = "Vy") ##roll curve
curve3 = p.plot(pen=pg.mkPen(color='r', width=2.0), name = "Vz") ##roll curve



windowWidth = 100   # width of the window displaying the curve
Vx = linspace(0, 0, windowWidth)   # create array that will contain the relevant time series
Vy = linspace(0, 0, windowWidth)   # create array that will contain the relevant time series
Vz = linspace(0, 0, windowWidth)   # create array that will contain the relevant time series
ptr = -windowWidth                       # set first x position
# Value = deque(maxlen=len(pitch))

# Realtime data plot.
# Each time this function is called, the data display is updated
def update():
    global curve, curve2, ptr, Vx, Vy, Vz
    data = ser.readline().decode("utf-8")

    if len(data) > 2:
        data = str(data)
        data = data[:-3]  # parse FW1.0 Data without space + \r\n
        splitData = data.split(',')
        if len(splitData) == 9:
            VxStr = splitData[0]
            VyStr = splitData[1]
            VzStr = splitData[2]
            Vx[:-1] = Vx[1:]  # shift pitch data in the temporal mean 1 sample left
            Vy[:-1] = Vy[1:]  # shift roll data in the temporal mean 1 sample left
            Vz[:-1] = Vz[1:]  # shift roll data in the temporal mean 1 sample left

            Vx[-1] = float(VxStr)   # vector containing the instantaneous values
            Vy[-1] = float(VyStr)   # vector containing the instantaneous values
            Vz[-1] = float(VzStr)   # vector containing the instantaneous values
            ptr += 1  # update x position for displaying the curve
            curve.setData(Vx)  # set the curve with these data
            curve2.setData(Vy)  # set the curve with these data
            curve3.setData(Vz)  # set the curve with these data
            # curve.setPos(ptr, 0)  # set x posiYtion in the graph to 0
            QtGui.QApplication.processEvents()  # process the plot now
### MAIN PROGRAM ###
# this is a brutal infinite loop calling the realtime data plot
while True:
    update()

### END QtApp ###
pg.QtGui.QApplication.exec_() # you MUST put this at the end

##################

