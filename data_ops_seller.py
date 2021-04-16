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

# Base = declarative_base()
# engine = create_engine('mysql+mysqlconnector://user:password@localhost:3306/DSTRY')
# Session = sessionmaker(bind=engine)
# session = Session()


# '''
# EXPECTED KEYS - name, username, emailid, password
# '''
# def signup_seller(msg):
# 	name=msg["name"]
# 	username = msg["username"]
# 	emailid = msg["emailid"]
# 	password = msg["password"]

# 	# update seller table
# 	item = Seller(name=name, username=username, emailid=emailid, password=password)
# 	session.add(item)
# 	session.commit()
# 	print("signup seller ----------------------------")
	
# 	ret = {"ack":True, "error":""}
# 	return ret


# '''
# EXPECTED KEYS - username
# '''
# def login_seller(msg):
# 	username = msg["username"]
# 	results = session.query(Seller).filter_by(username=username).all()
# 	print(results)
# 	ret = {"ack":True, "error":""}
# 	if(len(results)!=0):
# 		ret['password'] = results[0].password
# 	else:
# 		ret["password"] = None
# 	print(ret)
# 	return ret

# '''
# EXPECTED KEYS - username, product_type, product_name, price, quantity
# '''
# def add_product(msg):
# 	username = msg["username"]
# 	product_type = msg["product_type"]
# 	product_name = msg["product_name"]
# 	price = msg["price"]
# 	quantity = msg["quantity"]


# 	results = session.query(Seller).filter_by(username=username).all()[0]
	
# 	item = Product(
# 				seller=results, 
# 				type=product_type,
# 				name=product_name,
# 				price=price,
# 				quantity=quantity,
# 			)
# 	session.add(item)
# 	session.commit()
# 	ret = {"ack":True, "error":""}
# 	print("add product ----------------------------")	
# 	return ret
