import socket
import struct
import json
import urllib.request

# print("enter public ip of host : ")
# HOST = input().replace(" ", "").replace('\n', "")
PORT = 1104
url = "https://gist.githubusercontent.com/sanketRmeshram/2e0c71add59402cc26f1a518e425e0a8/raw/all_ip.txt"
HOST = [_.decode("utf-8").replace(" ", "").replace('\n', "") for _ in urllib.request.urlopen(url)]
total_node = len(HOST)
index = 0
print(HOST)


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST[index], PORT)) 
    msg = input()
    msg = {
        "isRead" : True,
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

    index = (index+1)%total_node


