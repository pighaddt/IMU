import serial
##

# target_name = "LAIRD BL654-3D1EBA"
# target_address = "d3021c3d1eba" # Touch Taiwan Device ()
#
# nearby_devices = bluetooth.discover_devices()
# print(nearby_devices)
# print()
#
# for bdaddr in nearby_devices:
#     if target_name == bluetooth.lookup_name(bdaddr):
#         target_address = bdaddr
#         break
#
# if target_address is not None:
#     print("Found target bluetooth device with address: ", target_address)
# else:
#     print("Could not find target bluetooth device nearby")


# ser = serial.Serial("d3021c3d1eba", 9600)
# while True:
#     result = ser.read()
#     print (result)

##
# import serial
# import types
#
portx = "COM5"
bps = 115200

A = []
ser = serial.Serial(portx, int(bps), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
if (ser.isOpen()):
    print("open success")
    while (True):
        line = ser.readline().decode("utf-8")
        # a = str(line)
        a = line
        # print(a)
        data = a[:-3]
        # print(data)
        splitData = data.split(',')
        print(splitData)
        print(len(splitData))
        # pitch = splitData[0]
        # print(pitch[2:])

        # a = a.encode('utf-8').strip()

        # print(line.decode('utf-8'))
        # if(line):
        #     a = str(line)
        #     # a = bytes.decode('utf-8')
        # if data != '\n':
        #     print(data)
        # #     line = 0

else:
    print("open failed")

ser.close()



