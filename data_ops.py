import json
from data_ops_seller import *
from data_ops_buyer import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

## msg - is the msg recvd by sanket
## expected to be a string

engine = create_engine('mysql+mysqlconnector://user:password@localhost:3306/DSTRY')
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

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
	if(msg['method'] == "view_cart"):
		return view_cart(msg)	
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
	
	# signup seller check
	# msg_handler(json.dumps(test_json['signup_seller1']))
	# msg_handler(json.dumps(test_json['signup_seller2']))

	# # test login seller
	# msg_handler(json.dumps(test_json['login_seller1']))


	# # add
	# msg_handler(json.dumps(test_json['add_product1']))
	# msg_handler(json.dumps(test_json['add_product2']))
	
	# msg_handler(json.dumps(test_json['view_all_products']))
	# msg_handler(json.dumps(test_json['filter_products1']))


	# # signup buyer check
	# msg_handler(json.dumps(test_json['signup_buyer1']))
	# msg_handler(json.dumps(test_json['signup_buyer2']))

	# # test login seller
	# msg_handler(json.dumps(test_json['login_buyer1']))


	# # add
	# msg_handler(json.dumps(test_json['add_to_cart1']))	
	msg_handler(json.dumps(test_json['view_cart1']))

	# update quantity
	msg_handler(json.dumps(test_json['update_quantity1']))
	msg_handler(json.dumps(test_json['view_cart1']))
	
	# # should produce error
	# msg_handler(json.dumps(test_json['update_quantity2']))
	# msg_handler(json.dumps(test_json['view_cart1']))

	# success checkout
	msg_handler(json.dumps(test_json['checkout1']))
	msg_handler(json.dumps(test_json['view_cart1']))

	# failure checkout
	msg_handler(json.dumps(test_json['add_to_cart3']))	
	msg_handler(json.dumps(test_json['checkout2']))

	session.close()
	# meta = MetaData()
	# meta.reflect(bind=engine)
	# for table in reversed(meta.sorted_tables):
	# 	print(table)
	# 	table.drop(engine)

if __name__ == '__main__':
	main()