import socket

HOST = "192.168.91.128"   # The remote host
PORT = 30002              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

for i in range(2):
    data = s.recv(32768)
    print ("Received", data)

s.close()
