from socket import *

server = socket(AF_INET, SOCK_STREAM)
server.connect(("localhost", 10005))
server.send(bytes([0x0a]))

a = server.recv(512)
print(a)