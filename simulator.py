from socket import *

ACK = 0x00
REQ_PKT_HEADER = 0x0a

server = socket(AF_INET, SOCK_STREAM)
server.connect(("localhost", 10041))
server.send(bytes([REQ_PKT_HEADER]))
print("Presentation response:")
print(server.recv(512))
while True:
    print("Data: ")
    data = server.recv(512)
    print("Header: " + str(data[0]))
    print("Time: " + str(data[1:4]))
    print("Alarm: " + str(data[5]))
    print("Sensor value" + str(data[6:9]))
   # print(server.recv(512))
    server.send(bytes([ACK]))


#print(int.from_bytes(int(time.mktime(datetime.now().timetuple())).to_bytes(4, byteorder = "little"), byteorder= "little"))