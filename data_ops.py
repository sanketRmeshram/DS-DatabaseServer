import json
from data_ops_seller import *
from data_ops_buyer import *

## msg - is the msg recvd by sanket
## expected to be a string

def msg_handler(msg):
	msg = json.loads(msg)

	# each method will return json dumped in form of string

	#### SELLER
	if(msg['method'] == "signup_seller"):	
		return signup_seller(msg)
	if(msg['method'] == "login_seller"):	
		return login_seller(msg)
	if(msg['method'] == "add_product"):	
		return add_product(msg)
	
	#### BUYER
	if(msg['method'] == "signup_buyer"):	
		return signup_buyer(msg)
	if(msg['method'] == "login_buyer"):	
		return login_buyer(msg)
	if(msg['method'] == "view_all_products"):
		return view_all_products(msg)	
	if(msg['method'] == "filter_products"):
		return filter_products(msg)	
	if(msg['method'] == "add_to_cart"):
		return add_to_cart(msg)	
	if(msg['method'] == "update_quantity"):
		return update_quantity(msg)
	if(msg['method'] == "checkout"):
		return checkout(msg)

	ret = {"ack":True, "error":"ERROR - INCORRECT MSG FORMAT"}
	return json.dumps(ret)


def main():
	print("--------------------------------------------------------------")
	with open("test_data_ops.json") as f:
		test_json = json.load(f)
	
	print(test_json)

	# test login seller
	msg_handler(json.dumps(test_json['login_seller']))

if __name__ == '__main__':
	main()