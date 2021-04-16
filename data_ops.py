import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data_stuff import (
    Buyer,
    Seller,
    Product,
    Admin,
    Cart,
    Transaction
)
# logging.basicConfig()
# logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://user:password@localhost:3306/DSTRY')
Session = sessionmaker(bind=engine)
session = Session()



## msg - is the msg recvd by sanket 
def msg_handler(msg):
	msg = json.loads(msg)

	# each method will return json dumped in form of string

	#### SELLER
	if(msg['method'] == "get_product"):	
		return get_product(msg)
	if(msg['method'] == "update_product"):
		return update_product(msg)
	
	#### BUYER
	if(msg['method'] == "view_all_products"):
		return view_all_products(msg)	
	if(msg['method'] == "view_product"):
		return view_product(msg)	
	if(msg['method'] == "add_product"):
		return add_product(msg)	
	if(msg['method'] == "update_quantity"):
		return update_quantity(msg)	
	if(msg['method'] == "remove_product"):
		return remove_product(msg)
	if(msg['method'] == "checkout"):
		return checkout(msg)

	ret = {"ack":True, "error":"ERROR - INCORRECT MSG FORMAT"}
	return json.dumps(ret)


#### SELLER

'''
EXPECTED KEYS - seller_id
'''
def get_product(msg):
	return ret

'''
EXPECTED KEYS - seller_id, product_id
'''
def update_product(msg):
	return ret


##### BUYER 


'''
EXPECTED KEYS - none
'''
def view_all_products(msg):
	return ret

'''
EXPECTED KEYS - product_id
'''
def view_product(msg):
	return ret


'''
EXPECTED KEYS - product_id
'''
def add_product(msg):
	return ret


'''
EXPECTED KEYS - product_id, user_id
'''
def add_product(msg):
	return ret


'''
EXPECTED KEYS - product_id, new_quantity, user_id
'''
def update_quantity(msg):
	return ret

'''
EXPECTED KEYS - product_id, new_quantity=0, user_id
'''
def remove_product(msg):
	return ret


'''
EXPECTED KEYS - product_id, user_id
'''
def checkout(msg):
	return ret