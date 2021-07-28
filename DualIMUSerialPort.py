import serial

portxBT01 = "COM8"
portxBT02 = "COM4"
bpsBT1 = 115200
bpsBT2 = 115200

serBT1 = serial.Serial(portxBT01, int(bpsBT1), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
serBT2 = serial.Serial(portxBT02, int(bpsBT2), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
if (serBT1.isOpen() & serBT2.isOpen()):
    print("open success")
    while (True):
        lineBT1 = serBT1.readline().decode("utf-8")
        print("BT01 : " + lineBT1)
        lineBT2 = serBT2.readline().decode("utf-8")
        print("BT02 : " + lineBT2)

else:
    print("open failed")

serBT1.close()
serBT2.close()



