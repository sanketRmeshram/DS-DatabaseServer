import socket
import struct
import json

print("enter public ip of host : ")
HOST = input().replace(" ", "").replace('\n', "")
PORT = 1104

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True :
    msg = input()
    msg = {
        "sanket" : msg
    }
    msg = json.dumps(msg)
    msg = msg.encode('utf-8')
    msg_sz = struct.pack(">H", len(msg))
    s.sendall(msg_sz+msg)
    print("sended")





