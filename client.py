import socket
import struct

HOST = local_ip = socket.gethostbyname(socket.gethostname())
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True :
    msg = input()
    msg = msg.encode('utf-8')
    msg_sz = struct.pack(">H", len(msg))
    s.sendall(msg_sz+msg)
    print("sended")





