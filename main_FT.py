
import socket
import logging
import threading
import time
from queue import Queue
import struct
import json 
import heapq
import urllib.request
from data_ops import msg_handler

public_ip = None
local_ip = None
server_socket = None
local_port = None
local_index = None
list_of_ip_port = None 
total_node = None
accepted_connection = None
joined_connection = None
ip_mapping_to_index = None 
send_queue = None #everything will be string inside queue
send_queue_lock = None
request_id = None 
timestamp = None
timestamp_lock = None
message_id =None
message_id_lock = None
task_queue = None
task_queue_lock = None
completed_atomic_multicast = None 
completed_atomic_multicast_lock = None
message_id_to_message = None
message_id_to_message_lock = None
atomic_multicast_ACKD_timestamps = None
atomic_multicast_ACKD_timestamps_lock = None
operation_lock = None
completed_request = None
completed_request_lock = None 
req_id_to_response = None 
req_id_to_response_lock = None 
isAlive = None
total_alive_node = None 
isAlive_lock = None
total_alive_node_lock = None

def init():
    global public_ip
    global local_ip
    global server_socket 
    global local_port 
    global local_index
    global list_of_ip_port 
    global total_node
    global accepted_connection 
    global joined_connection 
    global ip_mapping_to_index 
    global send_queue
    global send_queue_lock
    global request_id
    global message_id
    global message_id_lock
    global timestamp
    global timestamp_lock
    global task_queue    #(timestamp,is_confirmed,msg_id)
    global task_queue_lock
    global completed_atomic_multicast 
    global completed_atomic_multicast_lock 
    global message_id_to_message
    global message_id_to_message_lock
    global atomic_multicast_ACKD_timestamps
    global atomic_multicast_ACKD_timestamps_lock 
    global operation_lock
    global completed_request
    global completed_request_lock
    global req_id_to_response
    global req_id_to_response_lock
    global isAlive
    global total_alive_node
    global isAlive_lock
    global total_alive_node_lock

    # local_ip = open("my_ip.txt",'r').readline().replace(" ","")

    local_ip = socket.gethostbyname(socket.gethostname())
    # public_ip = open("my_ip.txt", 'r').readline().replace(" ", "").replace('\n',"")

    # print("Enter your own public ip : ")
    # public_ip = input().replace(" ", "").replace('\n', "")
    public_ip = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read())['ip']
    print("public ip : " , public_ip)

    server_socket = None
    local_port = 1104
    url = "https://gist.githubusercontent.com/sanketRmeshram/2e0c71add59402cc26f1a518e425e0a8/raw/all_ip.txt"
    list_of_ip_port = [(_.decode("utf-8").replace(" ", "").replace('\n', ""), local_port) for _ in urllib.request.urlopen(url)]
    print(list_of_ip_port)
    total_node = len(list_of_ip_port)
    accepted_connection = [None for _ in range(total_node)]
    joined_connection = [None for _ in range(total_node)]
    ip_mapping_to_index = {}

    for i in range(total_node):
        ip_mapping_to_index[list_of_ip_port[i][0]] = i
    local_index = ip_mapping_to_index[public_ip]
    send_queue = [Queue() for _ in range(total_node)]
    send_queue_lock = [threading.Lock() for _ in range(total_node)]
    request_id = 0
    message_id = 0
    timestamp = 0
    timestamp_lock = threading.Lock()
    message_id_lock = threading.Lock()
    task_queue = []
    task_queue_lock = threading.Lock()
    completed_atomic_multicast = set()
    completed_atomic_multicast_lock = threading.Lock()
    message_id_to_message = {}
    message_id_to_message_lock = threading.Lock()
    atomic_multicast_ACKD_timestamps = {}
    atomic_multicast_ACKD_timestamps_lock = threading.Lock()

    operation_lock = threading.Lock()

    completed_request = set()
    completed_request_lock = threading.Lock()
    req_id_to_response = {}
    req_id_to_response_lock = threading.Lock()

    isAlive = [True for _ in range(total_node)]
    total_alive_node = total_node
    isAlive_lock = [threading.Lock() for _ in range(total_node)]
    total_alive_node_lock = threading.Lock()


    print(list_of_ip_port)
    print(ip_mapping_to_index)

    print(local_ip, public_ip)


def accept_request_thread(list_of_ip_port) :
    global server_socket
    global accepted_connection
    global ip_mapping_to_index
    logging.info("in accept_request_thread")
    for _ in range(len(list_of_ip_port)):
        conn, addr = server_socket.accept()
        print("accepted  : ",addr)
        accepted_connection[ip_mapping_to_index[addr[0]]] =(conn, addr[0])
        

def send_request_thread(list_of_ip_port) :
    global joined_connection
    global ip_mapping_to_index
    logging.info("in send_request_thread")
    for ip,port in list_of_ip_port :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip,port))
        joined_connection[ip_mapping_to_index[ip]] = (sock, ip)


def handle(msg,index) :
    '''
            msg = {
            "time" : now,
            "type" : "PrepareAtomicMulticast" ,
            "msg_id" : str(local_index)+"_"+str(msg_id),
            "content" : request


        }
    '''

    global timestamp
    global timestamp_lock

    global task_queue
    global task_queue_lock

    global send_queue_lock
    global send_queue

    global completed_atomic_multicast
    global completed_atomic_multicast_lock

    global message_id_to_message
    global message_id_to_message_lock

    global atomic_multicast_ACKD_timestamps
    global atomic_multicast_ACKD_timestamps_lock

    global isAlive
    global total_alive_node
    global total_alive_node_lock

    if msg["type"] == "PrepareAtomicMulticast" :

        timestamp_lock.acquire()

        timestamp = max(timestamp+1,msg["time"]+1)
        now = timestamp

        task_queue_lock.acquire()
        heapq.heappush(task_queue, (now,0,msg["msg_id"]))
        task_queue_lock.release()

        timestamp_lock.release()



        message_id_to_message_lock.acquire()
        message_id_to_message[msg["msg_id"]] = msg["content"] 
        message_id_to_message_lock.release()

        reply = {
            "time" : now,
            "type": "ACKAtomicMulticast",
            "msg_id": msg["msg_id"],

        }

        reply = json.dumps(reply)

        send_queue_lock[index].acquire()
        send_queue[index].put(reply)
        send_queue_lock[index].release()

        return 
    
    if msg["type"] == "ACKAtomicMulticast" :


        max_time = None
        atomic_multicast_ACKD_timestamps_lock.acquire()
        if msg["msg_id"] in atomic_multicast_ACKD_timestamps :
            atomic_multicast_ACKD_timestamps[msg["msg_id"]].append(msg["time"])
        else :
            atomic_multicast_ACKD_timestamps[msg["msg_id"]] = [msg["time"]]
        total_alive_node_lock.acquire()
        if len(atomic_multicast_ACKD_timestamps[msg["msg_id"]])==total_alive_node :
            max_time = max(atomic_multicast_ACKD_timestamps[msg["msg_id"]])
        total_alive_node_lock.release()
        atomic_multicast_ACKD_timestamps_lock.release()
        if max_time is None :
            return
        
        reply = {
            "time": max_time,
            "type": "FinalAtomicMulticast",
            "msg_id": msg["msg_id"],
        }

        reply = json.dumps(reply)

        for i in range(total_node):
            if isAlive[i]==False :
                continue
            send_queue_lock[i].acquire()
            send_queue[i].put(reply)
            send_queue_lock[i].release()
        return
    if msg["type"] == "FinalAtomicMulticast":


        task_queue_lock.acquire()
        heapq.heappush(task_queue, (msg["time"],1,msg["msg_id"]))
        task_queue_lock.release()   
        


        completed_atomic_multicast_lock.acquire()
        completed_atomic_multicast.add(msg["msg_id"])
        completed_atomic_multicast_lock.release()

        return






def read_thread(conn,index,ip):
    logging.info("inside read_thread with index : %d  , ip : %s ", index, ip)
    global isAlive
    global isAlive_lock
    global total_alive_node
    global total_alive_node_lock
    try :

        while True :
            sz = conn.recv(2)
            sz = struct.unpack(">H", sz)[0]
            msg = conn.recv(sz)    # There is possibility that it may not work so just create a loop and take constant size except last one #
            msg = msg.decode('utf-8')
            msg = json.loads(msg)
            logging.info("just recieved : %s from %s",json.dumps(msg),ip)
            handle(msg,index)
        pass
    except :
        isAlive_lock[index].acquire()
        total_alive_node_lock.acquire()
        if isAlive[index] :
            isAlive[index] = False
            total_alive_node-=1
        total_alive_node_lock.release()
        isAlive_lock[index].release()
        


def write_thread(conn,index,ip) :
    logging.info("inside write_thread with index : %d  , ip : %s ", index, ip)
    global send_queue_lock
    global send_queue
    global isAlive
    global isAlive_lock
    global total_alive_node
    global total_alive_node_lock
    try :
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
    except :
        isAlive_lock[index].acquire()
        total_alive_node_lock.acquire()
        if isAlive[index] :
            isAlive[index] = False
            total_alive_node-=1
        total_alive_node_lock.release()
        isAlive_lock[index].release()



def serve_request_thread(conn,req_id):
    logging.info("inside serving request : %d ",req_id)
    global timestamp
    global timestamp_lock
    global message_id
    global message_id_lock
    global send_queue_lock
    global send_queue
    global completed_request
    global req_id_to_response
    global req_id_to_response_lock
    global operation_lock
    global isAlive
    sz = conn.recv(2)
    sz = struct.unpack(">H", sz)[0]
    # print(sz)
    request_from_web_server = conn.recv(sz)
    request_from_web_server = request_from_web_server.decode('utf-8')
    request_from_web_server = json.loads(request_from_web_server)
    request = {
        "request_id" : req_id,
        "content" : request_from_web_server
    }
    logging.info("Recieved : %s from request id  %d", json.dumps(request_from_web_server), req_id)
    if request_from_web_server["type"]=='read' :
        operation_lock.acquire()
        response = dummy_execute(request_from_web_server)
        operation_lock.release()
        response = json.dumps(response)

        response = response.encode('utf-8')

        response_sz = struct.pack(">H", len(response))
        conn.sendall(response_sz+response)
        conn.close()

        return 

        

        



    timestamp_lock.acquire()
    timestamp+=1
    now = timestamp
    timestamp_lock.release()



    message_id_lock.acquire()
    message_id+=1
    msg_id = message_id
    message_id_lock.release()

    msg = {
        "time" : now,
        "type" : "PrepareAtomicMulticast" ,
        "msg_id" : str(local_index)+"_"+str(msg_id),
        "content" : request


    }
    msg = json.dumps(msg)


    ##############Atomic Multicast#####################################
    for i in range(total_node):
        if isAlive[i] == False :
            continue
        send_queue_lock[i].acquire()
        send_queue[i].put(msg)
        send_queue_lock[i].release()
    ##############Atomic Multicast#####################################

    while req_id not in completed_request :
        pass
    req_id_to_response_lock.acquire()
    response = req_id_to_response[req_id]
    req_id_to_response_lock.release()
    
    response = json.dumps(response)

    response = response.encode('utf-8')

    response_sz = struct.pack(">H", len(response))
    conn.sendall(response_sz+response)
    conn.close()
    


def dummy_execute(msg) :

    try :
        responce = msg_handler(msg)
        return responce
    except Exception as e :
        logging.info(e)
        return {
            'error' : e
        }

def executor_thread() :
    logging.info("inside executor thread")
    global task_queue
    global task_queue_lock
    global message_id_to_message
    global message_id_to_message_lock
    global operation_lock
    global completed_request
    global completed_request_lock
    global req_id_to_response
    global req_id_to_response_lock
    global isAlive

    while True :

        while not task_queue :
            pass

        task_queue_lock.acquire()
        op = heapq.heappop(task_queue)
        task_queue_lock.release()

        if op[1]==1 :



            message_id_to_message_lock.acquire()
            task = message_id_to_message[op[2]] 
            message_id_to_message_lock.release()
            ### Remember task is actually a JSON
            logging.info("executing : %s ",json.dumps(task))

            operation_lock.acquire()
            response = dummy_execute(task["content"])
            operation_lock.release()

            #execute here
            if int(op[2].split('_')[0]) == local_index :

                req_id_to_response_lock.acquire()
                req_id_to_response[task["request_id"]] = response
                req_id_to_response_lock.release()

                completed_request_lock.acquire()
                completed_request.add(task["request_id"])
                completed_request_lock.release()
            logging.info("executed : %s ", json.dumps(task))
        else :
            index_of_initiator = op[2].split('_')[0]
            while (op[2] not in completed_atomic_multicast) and isAlive[index_of_initiator] :
                pass



    

def main():

    
    global local_ip
    global server_socket
    global local_port
    global list_of_ip_port

    global ip_mapping_to_index
    global total_node

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    init()
    
    print("local ip : ", local_ip)
    

    #################################Temp##########################################
    # print("enter the port :") # no need if we are running on different machine
    # local_port = int(input())
    # # No need to take this as input just keep it same for all .
    #################################Temp##########################################


    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_ip,local_port))
    server_socket.listen()
    logging.info("you have successfully created the server.")
    logging.info("waiting for everyone to be ready . After everyone is ready press ENTER")

    input()
    


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

    print(ip_mapping_to_index)
    print(joined_connection)
    print(accepted_connection)
    ########################Temp##################################
    # ind = total_node
    # for i in accepted_connection:
    #     threading.Thread(target=read_thread, args=(i[0], ind, i[1],)).start()
    #     ind = (ind+1)%2
    # for i in joined_connection:
    #     threading.Thread(target=write_thread, args=(i[0], ind, i[1],)).start()
    #     ind = (ind+1)%2
    ########################Temp##################################

    threading.Thread(target=executor_thread, args=()).start()

    print("press enter to start accepting  request from web server")
    input()
    print("Now i can accept the request from web-server")
    global request_id
    while True :
        conn, addr = server_socket.accept()
        request_id+=1
        threading.Thread(target=serve_request_thread, args=(conn,request_id,)).start()
        

    return 0

if __name__ == "__main__":

    main()

