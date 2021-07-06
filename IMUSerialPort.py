# import QtGui as QtGui
from PyQt5 import QtGui

import serial
import numpy as np
from numpy import *
from pyqtgraph.Qt import *
import pyqtgraph as pg
import serial
# from PhysioNetData import medianFilter, bandStopFilter
from collections import deque
import types

vx = []
vy = [0]
vz = [0]

ax = []
ay = []
az = []

portx = "COM10"
bps = 115200

A = []
ser = serial.Serial(portx, int(bps), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
# if (ser.isOpen()):
#     print("open success")
#     while (True):
#         line = ser.readline()
#         a = str(line)
#         data = a[2:-6]
#         x = data.split(',')
#         # a = a.encode('utf-8').strip()
#
#         # print(line.decode('utf-8'))
#         # if(line):
#         #     a = str(line)
#         #     # a = bytes.decode('utf-8')
#         # print(data)
#         print(data.split(','))
#         if(len(data)> 0):
#             if(len(data) >= 1 ):
#                 # print(x[0])
#                 vx.append(x[0])
#                 print("vx = " + str(vx))
#
#         #     line = 0
#
# else:
#     print("open failed")
#
# ser.close()

### START QtApp #####
app = QtGui.QApplication([])            # initialize things
####################

R = 30
Y_range = [-100, 100]
win = pg.GraphicsWindow(title="Signal from IMU")  # create a window
win.setBackground('w')
p = win.addPlot(title="Realtime plot")  # create empty space for the plot in the window
p.setYRange(min=int(Y_range[0]), max=int(Y_range[1]))

# p2 = win.addPlot(title="RMS plot")  # create empty space for the plot in the window
# p2.setYRange(min=int(Y_range[0]), max=int(Y_range[1]))
curve = p.plot(pen=pg.mkPen(color='k', width=1.0))
curve2 = p.plot(pen=pg.mkPen(color='b', width=0.5))
windowWidth = 100
Xm = linspace(0, 0, 100)
# windowWidth = 100                       # width of the window displaying the curve
# Xm = linspace(0, 0, 250)         # create array that will contain the relevant time series
ptr = -windowWidth                       # set first x position
Value = deque(maxlen=len(Xm))

# Realtime data plot.
# Each time this function is called, the data display is updated
def update():
    global curve, ptr, Xm
    value = ser.readline()
    # value = str(ser.readline(), 'utf-8')
    print("value :" + str(value))
    # Raw signal
    # if value != '\r\n':
    if(len(value)> 1):
        Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
        print(value)
        a = str(value)
        data = a[2:-6]
        x = data.split(',')
        print("x = " + str(x))
        print("x = " + x[0])
        Xm[-1] = x[0]             # vector containing the instantaneous values

    # # Filtered signal: Median Filter to solve Baseline Wandering.
    # if value != '\r\n':
    #     print(value)
    #     Value.append(float(value))
    # if Value[-1] != 0:
    #     for i in range(len(Value)):
    #         med = np.median(Value)
    #     Xm[-1] = Value[-1] - med

    ptr += 1                              # update x position for displaying the curve
    curve.setData(Xm)                     # set the curve with these data
    curve.setPos(ptr, 0)                  # set x position in the graph to 0
    QtGui.QApplication.processEvents()    # process the plot now


### MAIN PROGRAM ###
# this is a brutal infinite loop calling the realtime data plot
while True:
    update()

### END QtApp ###
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################
