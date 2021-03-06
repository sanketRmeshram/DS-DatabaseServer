import logging
from sqlalchemy import create_engine
from sqlalchemy import update, delete
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


####################################################  BUYER OPS ######################################################################################
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

	ret = {"ack":True, "error":""}
	return ret


'''
EXPECTED KEYS - username
'''
def login_buyer(msg):
	username = msg["username"]
	results = session.query(Buyer).filter_by(username=username).all()
	logging.info("login_buyer -----------------")
	logging.info(results)

	ret = {"ack":True, "error":""}
	if(len(results)!=0):
		ret['password'] = results[0].password
	else:
		ret["password"] = None
	return ret


'''
EXPECTED KEYS - none
'''
def view_all_products(msg):
	results = session.query(Product).all()

	ret = {"ack":True, "error":""}
	ret['username'] = []
	ret['product_type'] = []
	ret['product_name'] = []
	ret['price'] = []
	ret['quantity'] = []
	ret['id'] = []
	for x in results:
		ret['username'].append(x.seller.username)
		ret['product_type'].append(x.type)
		ret['product_name'].append(x.name)
		ret['price'].append(x.price)
		ret['quantity'].append(x.quantity)
		ret['id'].append(x.id)
	logging.info("View products ----------------------------")
	logging.info(results)
	logging.info(ret)
	return ret


'''
EXPECTED KEYS - product_type
'''
def filter_products(msg):
	product_type = msg["product_type"] 
	results = session.query(Product).filter_by(type=product_type).all()
	
	ret = {"ack":True, "error":""}
	ret['username'] = []
	ret['product_type'] = []
	ret['product_name'] = []
	ret['price'] = []
	ret['quantity'] = []
	ret['id'] = []
	
	for x in results:
		ret['username'].append(x.seller.username)
		ret['product_type'].append(x.type)
		ret['product_name'].append(x.name)
		ret['price'].append(x.price)
		ret['quantity'].append(x.quantity)
		ret['id'].append(x.id)

	logging.info("Filter products ----------------------------")
	logging.info(results)
	logging.info(ret)
	return ret


'''
EXPECTED KEYS - product_id, username, quantity
'''
def add_to_cart(msg):
	product_id = msg["product_id"]
	username = msg["username"]
	quantity = msg["quantity"]
	ret = {"ack":True, "error":""}

	user = session.query(Buyer).filter_by(username=username).all()[0]
	product = session.query(Product).filter_by(id=product_id).all()[0]
	
	if(product.quantity>=1):
		already_exists = session.query(Cart).filter_by(product_id=product_id, user_id=user.id).all()
		if(len(already_exists)>0):
			if(product.quantity >= already_exists[0].quantity+1):
				stmt = update(Cart).where(Cart.product_id==product_id).where(Cart.user_id==user.id).values(quantity=already_exists[0].quantity+1).execution_options(synchronize_session="fetch")
				result = session.execute(stmt)
				session.commit()
				return ret
			else:
				ret['error'] = "QUANTITY_ERROR"
				return ret

		item = Cart(product=product, quantity=quantity, user_id=user.id)
		session.add(item)
		session.commit()
		logging.info("\nadd_to__cart products ----------------------------")
		return ret
	
	ret['error'] = "QUANTITY_ERROR"
	return ret


'''
EXPECTED KEYS - username
'''
def view_cart(msg):
	username = msg["username"]
	user_id = session.query(Buyer).filter_by(username=username).all()[0].id
	results = session.query(Cart).filter_by(user_id=user_id).all()

	ret = {"ack":True, "error":""}
	ret['product_id'] = []
	ret['quantity'] = []
	ret['name'] = []	
	
	for x in results:
		ret['product_id'].append(x.product.id)
		ret['quantity'].append(x.quantity)
		ret['name'].append(x.product.name)

	logging.info("\nview_cart products ----------------------------")
	logging.info(results)
	logging.info(ret)

	return ret

'''
EXPECTED KEYS - product_id, username, new_quantity
'''
def update_quantity(msg):
	product_id = msg["product_id"]
	username = msg["username"]
	new_quantity = msg["new_quantity"]
	ret = {"ack":True, "error":""}
	logging.info("update_quantity -------------------------")

	if(new_quantity==0):
		return remove_product(msg)

	quantity = session.query(Product).filter_by(id=product_id).all()[0].quantity

	# check if enough quantity is present
	if(quantity<new_quantity):
		ret['error'] = "QUANTITY_ERROR"
		logging.info(ret)
		return ret

	user_id = session.query(Buyer).filter_by(username=username).all()[0].id

	stmt = update(Cart).where(Cart.product_id == product_id).where(Cart.user_id==user_id).values(quantity=new_quantity).execution_options(synchronize_session="fetch")
	result = session.execute(stmt)
	session.commit()
	logging.info(ret)
	return ret

'''
EXPECTED KEYS - product_id, username
'''
def remove_product(msg):
	product_id = msg["product_id"]
	username = msg["username"]
	user_id = session.query(Buyer).filter_by(username=username).all()[0].id
	stmt = delete(Cart).where(Cart.product_id == product_id).where(Cart.user_id==user_id).execution_options(synchronize_session="fetch")
	result = session.execute(stmt)
	session.commit()
	ret = {"ack":True, "error":""}
	logging.info("remove_product -----------------")
	return ret


'''
EXPECTED KEYS - product_id, username
'''
def checkout(msg):
	product_id = msg["product_id"]
	username = msg["username"]
	user_id = session.query(Buyer).filter_by(username=username).all()[0].id
	logging.info("checkout---------------------")

	#  get cart quantity and remaining quantity form product table
	cart_row = session.query(Cart).filter_by(product_id=product_id, user_id=user_id).all()[0]
	cart_quantity = cart_row.quantity
	quantity = cart_row.product.quantity

	ret = {"ack":True, "error":""}
	# check if enough quantity is present
	if(quantity<cart_quantity):
		ret['error'] = "QUANTITY_ERROR"
		item = Transaction(
				user_id=user_id, 
				product_id=product_id,
				quantity=cart_quantity,
				status=False, 
			)
		session.add(item)
		session.commit()
		logging.info(ret)
		return ret

	# update transaction, product, cart tables
	item = Transaction(
				user_id=user_id, 
				product_id=product_id,
				quantity=cart_quantity,
				status=True, 
			)
	session.add(item)
	session.commit()

	# remove from cart
	remove_product(msg)

	# update product table
	# if(quantity-cart_quantity==0):
	# 	stmt = delete(Product).where(Product.id == product_id).execution_options(synchronize_session="fetch")
	# 	logging.info(stmt)
	# 	result = session.execute(stmt)
	# 	session.commit()
	# 	return ret

	stmt = update(Product).where(Product.id==product_id).values(quantity=quantity-cart_quantity).execution_options(synchronize_session="fetch")
	print(stmt)
	result = session.execute(stmt)
	session.commit()
	return ret


####################################################  SELLER OPS ######################################################################################

'''
EXPECTED KEYS - name, username, emailid, password
'''
def signup_seller(msg):
	name=msg["name"]
	username = msg["username"]
	emailid = msg["emailid"]
	password = msg["password"]

	# update seller table
	item = Seller(name=name, username=username, emailid=emailid, password=password)
	session.add(item)
	session.commit()
	print("signup seller ----------------------------")
	
	ret = {"ack":True, "error":""}
	return ret


'''
EXPECTED KEYS - username
'''
def login_seller(msg):
	username = msg["username"]
	results = session.query(Seller).filter_by(username=username).all()
	print(results)
	ret = {"ack":True, "error":""}
	if(len(results)!=0):
		ret['password'] = results[0].password
	else:
		ret["password"] = None
	print(ret)
	return ret

'''
EXPECTED KEYS - username, product_type, product_name, price, quantity
'''
def add_product(msg):
	username = msg["username"]
	product_type = msg["product_type"]
	product_name = msg["product_name"]
	price = msg["price"]
	quantity = msg["quantity"]


	results = session.query(Seller).filter_by(username=username).all()[0]
	
	item = Product(
				seller=results, 
				type=product_type,
				name=product_name,
				price=price,
				quantity=quantity,
			)
	session.add(item)
	session.commit()
	ret = {"ack":True, "error":""}
	print("add product ----------------------------")	
	return ret