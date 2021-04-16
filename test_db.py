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
try:
    bhagat = Seller(name='aaryan bhagat', email='a@g.com', phone='123', password='3fg')
    ankit = Seller(name='ankit bagde', email='ankit@e.com', password='asd', phone='123')
    fan = Product(name='orient fan', price=34.5, quantity=2, seller=ankit)
    sanket = Buyer(name='sanket', email='f@gm.com', phone='34', address='sd', password='fg')
    vasu = Buyer(name='gurrram', email='sd@g.com', phone='45', address='sddd', password='asd')
    bottle = Product(name='milton bottle', price=34.6, quantity=10, seller=ankit)
    shoes = Product(name='Puma shoes', price=100.45, quantity=1, seller=bhagat)
    session.add(bhagat)
    session.add(ankit)
    session.commit()
    print(ankit)
    print(bhagat)
    session.add(bottle)
    session.add(shoes)
    session.add(vasu)
    session.add(sanket)
    print(fan)
    print(fan.seller)
    print(bottle.seller)
    print(shoes.seller)
    cart_1 = Cart(user=ankit)
    cart_2 = Cart(user=ankit)
    cart_3 = Cart(user=ankit)

    session.add(cart_1)
    session.add(cart_2)
    session.add(cart_3)
    print(cart_1)
    print(cart_2)
    print(cart_3)
    # print(cart_1.user)
    print(cart_1.user)
    # print(cart_2.user)
    print(cart_2.user)
    # print(cart_3.user)
    print(cart_3.user)
finally:
    print('Deleting all')
    Base.metadata.drop_all(engine)
