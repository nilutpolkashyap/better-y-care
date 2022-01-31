import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
port_list = []
for p in ports:
    # print(p[0])
    port_list.append(p[0])

print(port_list)
