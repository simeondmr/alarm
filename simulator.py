from socket import *

ACK = 0x00
REQ_PKT_HEADER = 0x0a

server = socket(AF_INET, SOCK_STREAM)
server.connect(("localhost", 10021))
server.send(bytes([REQ_PKT_HEADER]))
print("Presentation response:")
print(server.recv(512))
while True:
    print("Data: ")
    print(server.recv(512))
    server.send(bytes([ACK]))


#print(int.from_bytes(int(time.mktime(datetime.now().timetuple())).to_bytes(4, byteorder = "little"), byteorder= "little"))