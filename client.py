import socket
import struct
import json

print("enter public ip of host : ")
HOST = input().replace(" ", "").replace('\n', "")
PORT = 1104

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

"""
read from database:

host = fdsafd
port = fsfds
connet
sz=sizeofmsginbyte
send sz+ msg

recv(2)
sz
reav(sz)
conn.close()

"""

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
    """
    read 2 bytes
    sz
    read(sz)
    conn.close()
    a = {

        "isRead" : 
        "Tables" :
    }
    

    web - DS MUlticast - Interpretor execute funtion return responce   - database fuction (update(table,primay, entry,jo modify karna ))

    """





