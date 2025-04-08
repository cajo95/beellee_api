from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Sequence, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import shortuuid

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    user_code = Column(String(100), nullable=False, unique=True, 
                      default=lambda: shortuuid.ShortUUID(alphabet="0123456789").random(length=10))
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    country = Column(String(100))
    city = Column(String(100))
    phone = Column(String(100), nullable=False, unique=True)
    date_created = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # relationships
    purchases = relationship("Purchases", back_populates="user")
    types = relationship("Type", back_populates="user")
    payment_types = relationship("Type_payment", back_populates="user")

class Purchases(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, Sequence('purchase_id_seq'), primary_key=True, autoincrement=True)
    user_code = Column(String(100), ForeignKey('users.user_code'), nullable=False)  # Changed to ForeignKey
    purchase_code = Column(String(100), nullable=False, unique=True)  # Fixed typo in column name
    number_items = Column(Integer)
    establishment = Column(String(100), nullable=True)
    type_payment_id = Column(Integer, ForeignKey('type_payment.id'))  # Fixed typo in column name
    total_payment = Column(Float, nullable=False)
    invoice_B64 = Column(Text)
    created_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("Users", back_populates="purchases")
    payment_type = relationship("Type_payment", back_populates="purchases")
    items = relationship("Items", back_populates="purchase")

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    purchase_code = Column(String(100), ForeignKey('purchases.purchase_code'))  # Fixed typo
    name = Column(String(100), nullable=False)
    value = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=True)
    type_id = Column(Integer, ForeignKey('types.id'))
    
    # Relationships
    purchase = relationship("Purchases", back_populates="items")
    item_type = relationship("Type", back_populates="items")

class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, Sequence('type_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    user_code = Column(String(100), ForeignKey('users.user_code'), nullable=False)  # Added ForeignKey
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("Users", back_populates="types")
    items = relationship("Items", back_populates="item_type")

class Type_payment(Base):
    __tablename__ = 'type_payment'

    id = Column(Integer, Sequence('type_payment_id_seq'), primary_key=True)  # Fixed sequence name
    name = Column(String(100), nullable=False)
    user_code = Column(String(100), ForeignKey('users.user_code'), nullable=False)  # Added ForeignKey
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("Users", back_populates="payment_types")
    purchases = relationship("Purchases", back_populates="payment_type")