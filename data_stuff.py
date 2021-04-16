from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    Boolean,
    ForeignKey,
    Float,
    DateTime
)

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship, backref

BUYER_TABLE_NAME = "buyer_table"
CART_TABLE_NAME = "cart_table"
PRODUCT_TABLE_NAME = "product_table"
ADMIN_TABLE_NAME = "admin_table"
SELLER_TABLE_NAME = "seller_table"
TRANSACTION_TABLE_NAME = "transaction_table"
REVIEW_TABLE_NAME = "review_table"

# Define the MySQL engine using MySQL Connector/Python
engine = create_engine('mysql+mysqlconnector://user:password@localhost:3306/DSTRY', echo=True)


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        value = list(self.__dict__.items())[1:]
        return str(value)


# Define and create the table
Base = declarative_base(cls=Base)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()


class Admin(Base):
    __tablename__ = ADMIN_TABLE_NAME
    id = Column(Integer, primary_key=True)
    password = Column(String(length=50))
    name = Column(String(length=50))
    email = Column(String(length=50))
    phone = Column(String(length=50))


class Seller(Base):
    __tablename__ = SELLER_TABLE_NAME
    id = Column(Integer, primary_key=True)
    password = Column(String(length=50))
    name = Column(String(length=50))
    email = Column(String(length=50))
    phone = Column(String(length=50))
    is_approved = Column(Boolean)
    products = relationship("Product", backref='seller')
    # profile
    # ratings


class Buyer(Base):
    __tablename__ = BUYER_TABLE_NAME
    id = Column(Integer, primary_key=True)
    password = Column(String(length=50))
    name = Column(String(length=50))
    emailid = Column(String(length=50))
    phone = Column(String(length=50))
    address = Column(String(length=200))
    username = Column(String(length=50))
    # given_reviews = relationship("Review", backref="user")
    # its_transactions = relationship("Transaction", backref="user")
    carts = relationship("Cart", back_populates="username")


class Product(Base):
    __tablename__ = PRODUCT_TABLE_NAME
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey(SELLER_TABLE_NAME + '.id'))
    # seller = relationship("Seller", back_populates="products")
    name = Column(String(length=50))
    # type
    # abg_rating
    price = Column(Float)
    quantity = Column(Integer)
    description = Column(String(length=300))
    reviews = relationship("Review", backref="product")
    # its_cart = relationship("Cart", backref="product")


class Review(Base):
    __tablename__ = REVIEW_TABLE_NAME
    id = Column(Integer, primary_key=True)
    comment = Column(String(300))
    product_id = Column(Integer, ForeignKey(PRODUCT_TABLE_NAME + '.id'))
    # product = relationship("Product", back_populates="reviews")
    # user_id = Column(Integer, ForeignKey(BUYER_TABLE_NAME + '.id'))
    # user = relationship("Buyer", back_populates="given_reviews")


class Transaction(Base):
    __tablename__ = TRANSACTION_TABLE_NAME
    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey(BUYER_TABLE_NAME + '.id'))
    # user = relationship("Buyer", back_populates="its_transactions")
    product_id = Column(Integer)
    quantity = Column(Integer)
    time = Column(DateTime)
    status = Column(Boolean)


class Cart(Base):
    __tablename__ = CART_TABLE_NAME
    id = Column(Integer, primary_key=True)
    # product_id = Column(Integer, ForeignKey(PRODUCT_TABLE_NAME + '.id'))
    # product = relationship("Product", back_populates="its_cart")
    user_id = Column(Integer, ForeignKey(BUYER_TABLE_NAME + '.id'))
    username = relationship("Buyer", back_populates="carts")
    quantity = Column(Integer)


Base.metadata.create_all(engine)
