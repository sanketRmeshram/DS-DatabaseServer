from requester_module import send_request

while True :
    s = input()
    msg = {
        "type" : "read",
        "content" : s
    }
    response = send_request(msg)
    print("recieved : " , response)