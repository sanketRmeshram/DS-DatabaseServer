import socket
import struct
import json

print("enter public ip of host : ")
HOST = input().replace(" ", "").replace('\n', "")
PORT = 1104



while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT)) 
    msg = input()
    msg = {
        "isRead" : False,
        "sanket": msg
    }
    msg = json.dumps(msg)
    msg = msg.encode('utf-8')
    msg_sz = struct.pack(">H", len(msg))
    s.sendall(msg_sz+msg)
    print("sended")
    sz = s.recv(2)
    sz = struct.unpack(">H", sz)[0]
    # print(sz)
    response = s.recv(sz)
    s.close() # very very  important
    response = response.decode('utf-8')
    response = json.loads(response)
    print("received : ",response)


