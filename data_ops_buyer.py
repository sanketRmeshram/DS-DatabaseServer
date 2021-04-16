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

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://user:password@localhost:3306/DSTRY')
Session = sessionmaker(bind=engine)
session = Session()

'''
EXPECTED KEYS - name, username, emailid, password
'''
def signup_buyer(msg):
	name=msg["name"]
	username = msg["username"]
	emailid = msg["emailid"]
	password = msg["password"]
	item = Buyer(name=name, username=username, emailid=emailid, password=password)
	session.add(item)
	session.commit()
	return ret


'''
EXPECTED KEYS - username
'''
def login_buyer(msg):
	username = msg["username"]
	results = session.query(Buyer).filter_by(name=username).all()
	print(results)
	return ret


'''
EXPECTED KEYS - none
'''
def view_all_products(msg):
	results = session.query(Product).all()
	return ret


'''
EXPECTED KEYS - product_type
'''
def filter_products(msg):
	product_type = msg["product_type"] 
	results = session.query(Product).filter_by(product_type=product_type).all()
	return ret


'''
EXPECTED KEYS - product_id, username, quantity
'''
def add_to_cart(msg):
	product_id = msg["product_id"]
	username = msg["username"]
	quantity = msg["quantity"]

	item = Cart(product_id=product_id, username=username, quantity=quantity)
	session.add(item)
	session.commit()
	
	return ret

'''
EXPECTED KEYS - product_id, username, new_quantity
'''
def update_quantity(msg):
	product_id = msg["product_id"]
	username = msg["username"]
	quantity = msg["new_quantity"]

	if(quantity==0):
		remove_product(msg)

	quantity = session.query(Product).filter_by(product_id=product_id).all()

	# check if enough quantity is present
	if(quantity<update_quantity):
		return ERROR
	
	stmt = update(Cart).where(Cart.product_id == product_id and Cart.username==username).values(quantity=quantity).execution_options(synchronize_session="fetch")
	result = session.execute(stmt)
	session.commit()
	return ret

'''
EXPECTED KEYS - product_id, user_id
'''
def remove_product(msg):
	product_id = msg["product_id"]
	username = msg["username"]

	stmt = delete(Cart).where(Cart.product_id == product_id and Cart.username==username).execution_options(synchronize_session="fetch")
	result = session.execute(stmt)
	session.commit()
	return ret


'''
EXPECTED KEYS - product_id, username
'''
def checkout(msg):
	
	return ret