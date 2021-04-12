
import socket
import logging
import threading
import time
from queue import Queue
import struct

local_ip = None
server_socket = None
local_port = None
list_of_ip_port = None 
total_node = None
accepted_connection = None
joined_connection = None
ip_mapping_to_index = None 
send_queue = None #everything will be string inside queue
send_queue_lock = None
request_id = None 

def init():
    global local_ip
    global server_socket 
    global local_port 
    global list_of_ip_port 
    global total_node
    global accepted_connection 
    global joined_connection 
    global ip_mapping_to_index 
    global send_queue
    global send_queue_lock
    global request_id
    

    local_ip = open("my_ip.txt",'r').readline().replace(" ","")

    # local_ip = socket.gethostbyname(socket.gethostname())

    server_socket = None
    local_port = 1104

    list_of_ip_port = [(_.replace(" ", ""), local_port) for _ in open("all_ip.txt", 'r')]

    total_node = len(list_of_ip_port)
    accepted_connection = [None for _ in range(total_node)]
    joined_connection = [None for _ in range(total_node)]
    ip_mapping_to_index = {}

    for i in range(total_node):
        ip_mapping_to_index[list_of_ip_port[i][0]] = i

    send_queue = [Queue() for _ in range(total_node)]
    send_queue_lock = [threading.Lock() for _ in range(total_node)]
    request_id = 0



def accept_request_thread(list_of_ip_port) :
    logging.info("in accept_request_thread")
    for _ in range(len(list_of_ip_port)):
        conn, addr = server_socket.accept()
        accepted_connection[ip_mapping_to_index[addr[0]]] =(conn, addr[0])
        

def send_request_thread(list_of_ip_port) :
    logging.info("in send_request_thread")
    for ip,port in list_of_ip_port :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip,port))
        joined_connection[ip_mapping_to_index[ip]] = (sock, ip)


def read_thread(conn,index,ip):
    logging.info("inside read_thread with index : %d  , ip : %s ", index, ip)
    while True :
        sz = conn.recv(2)
        sz = struct.unpack(">H", sz)[0]
        msg = conn.recv(sz)    # There is possibility that it may not work so just create a loop and take constant size except last one #
        msg = msg.decode('utf-8')
        logging.info("just recieved : %s from %s",msg,ip)
    pass

def write_thread(conn,index,ip) :
    logging.info("inside write_thread with index : %d  , ip : %s ", index, ip)
    while True :
        while send_queue[index].empty() :
            pass
        send_queue_lock[index].acquire()
        msg = send_queue[index].get()
        send_queue_lock[index].release()
        msg = msg.encode('utf-8')
        msg_sz = struct.pack(">H", len(msg)) # Short unsigned integer type. Contains at least the [0, 65,535] range.
        conn.sendall(msg_sz+msg)
    pass


def serve_request_thread(conn,request_id):
    logging.info("inside serving request : %d ",request_id)
    while True :
        sz = conn.recv(2)
        sz = struct.unpack(">H", sz)[0]
        print(sz)
        msg = conn.recv(sz)
        msg = msg.decode('utf-8')
        logging.info("Recieved : %s from request id  %d", msg, request_id)
        global send_queue_lock
        global send_queue
        for i in range(total_node):
            send_queue_lock[i].acquire()
            send_queue[i].put(msg)
            send_queue_lock[i].release()

def main():

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    init()
    global local_ip
    print("local ip : ", local_ip)
    global local_port

    #################################Temp##########################################
    # print("enter the port :") # no need if we are running on different machine
    # local_port = int(input())
    # # No need to take this as input just keep it same for all .
    #################################Temp##########################################


    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_ip,local_port))
    server_socket.listen()
    logging.info("you have successfully created the server.")
    logging.info("waiting for everyone to be ready . After everyone is ready press ENTER")

    input()
    
    global list_of_ip_port

    
    global ip_mapping_to_index
    global total_node

    print(ip_mapping_to_index)
    AR = threading.Thread(target=accept_request_thread, args=(list_of_ip_port,))
    SR = threading.Thread(target=send_request_thread, args=(list_of_ip_port,))
    AR.start()
    SR.start()

    AR.join()
    SR.join()

    logging.info("all connections established")

    for i in accepted_connection :
        threading.Thread(target=read_thread, args=(i[0], ip_mapping_to_index[i[1]], i[1],)).start()
    for i in joined_connection:
        threading.Thread(target=write_thread, args=(i[0], ip_mapping_to_index[i[1]], i[1],)).start()


    ########################Temp##################################
    # ind = total_node
    # for i in accepted_connection:
    #     threading.Thread(target=read_thread, args=(i[0], ind, i[1],)).start()
    #     ind = (ind+1)%2
    # for i in joined_connection:
    #     threading.Thread(target=write_thread, args=(i[0], ind, i[1],)).start()
    #     ind = (ind+1)%2
    ########################Temp##################################

    print("press enter to start acceptin  request from web server")
    input()
    global request_id
    while True :
        conn, addr = server_socket.accept()
        request_id+=1
        threading.Thread(target=serve_request_thread, args=(conn,request_id,)).start()
        

    return 0

if __name__ == "__main__":

    main()

