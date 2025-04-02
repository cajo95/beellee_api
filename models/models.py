from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Sequence, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from db.db import Base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    user_code = Column(String(100), nullable=False, unique=True)
    user_name = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    identification = Column(String(100), nullable=False, unique=True)
    country = Column(String(100))
    city = Column(String(100))
    address = Column(String(100))
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(100), nullable=False, unique=True)
    activity = Column(String(100))
    activity_type_id = Column(Integer, ForeignKey('activity_types.id'))
    income_type_id = Column(Integer, ForeignKey('income_types.id'))
    activated = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    activities = relationship("ActivityTypes", back_populates="users")

class Purchases(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, Sequence('purchase_id_seq'), primary_key=True, autoincrement=True)
    user_code = Column(String(100), ForeignKey('users.user_code'))
    purchese_code = Column(String(100), nullable=False, unique=True) # UUID
    payment_id = Column(Integer, ForeignKey('payments.id'))
    number_items = Column(Integer, nullable=False)
    total_payment = Column(Float, nullable=False)
    establishment = Column(String(100), nullable=True)
    installments = Column(Integer, nullable=True)
    invoice_B64 = Column(Text)
    date_time = Column(DateTime)  # Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    purchese_code = Column(String(100), ForeignKey('purchases.purchese_code'))
    name = Column(String(100), nullable=False)
    value = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=True)

class ActivityTypes(Base):
    __tablename__ = 'activity_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    alias = Column(String(100), nullable=False)
    users = relationship("Users", back_populates="activities")

class IncomeTypes(Base):
    __tablename__ = 'income_types'

    id = Column(Integer, primary_key=True)
    type = Column(String(100), nullable=False)
    alias = Column(String(100), nullable=False)

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, Sequence('income_id_seq'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    income_types_id = Column(Integer, ForeignKey('income_types.id'))
    days = Column(Integer, nullable=False)
    periodic_income = Column(Boolean, default=True)
    value = Column(Float, nullable=False)

class EventualIncome(Base):
    __tablename__ = 'eventual_income'

    id = Column(Integer, Sequence('eventual_income_id_seq'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    value = Column(Float, nullable=False)
    date_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, Sequence('payment_id_seq'), primary_key=True)
    type = Column(String(100), nullable=False)
