from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Sequence, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from db.db import Base

Base = declarative_base()

# class Users(Base):
#     __tablename__ = 'users'
#     id = Column(BigInteger, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
#     user_code = Column(String(100), nullable=False, unique=True)
#     user_name = Column(String(100), nullable=False, unique=True)
#     name = Column(String(100), nullable=False)
#     surname = Column(String(100), nullable=False)
#     identification = Column(String(100), nullable=False, unique=True)
#     country = Column(String(100))
#     city = Column(String(100))
#     address = Column(String(100))
#     email = Column(String(100), nullable=False, unique=True)
#     phone = Column(String(100), nullable=False, unique=True)
#     activity = Column(String(100))
#     activity_type_id = Column(Integer, ForeignKey('activity_types.id'))
#     income_type_id = Column(Integer, ForeignKey('income_types.id'))
#     activated = Column(Boolean, default=False)
#     date_created = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#     activities = relationship("ActivityTypes", back_populates="users")

class Purchases(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, Sequence('purchase_id_seq'), primary_key=True, autoincrement=True)
    user_code = Column(String(100), nullable=False) #UUID is 36 characters
    purchese_code = Column(String(100), nullable=False, unique=True)
    number_items = Column(Integer)
    establishment = Column(String(100), nullable=True)
    type_id = Column(Integer, ForeignKey('types.id'))  # Changed to proper foreign key
    total_payment = Column(Float, nullable=False)
    invoice_B64 = Column(Text)
    created_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    purchese_code = Column(String(100), ForeignKey('purchases.purchese_code'))
    name = Column(String(100), nullable=False)
    value = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=True)
    type_id = Column(Integer, ForeignKey('types.id'))  # Added type for items

class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, Sequence('type_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)