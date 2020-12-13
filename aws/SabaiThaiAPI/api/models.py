import os
from datetime import datetime

from sqlalchemy import (
    create_engine,
    MetaData,
    Column,
    Index,
    ForeignKey,
    Integer,
    Numeric,
    String,
    DateTime,
    Time,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DB_ENGINE', 'postgres://admin@localhost/SabaiThaiDB'))
Session = sessionmaker(engine)

Base = declarative_base(metadata=MetaData(schema='sabai_thai'))


class Price(Base):
    __tablename__ = 'price'
    __table_args__ = (
        Index('idx_type_duration_date', 'massage_type', 'duration', 'start_date')
    )
    id = Column(Integer, primary_key=True)
    massage_type = Column(String, nullable=False)
    duration = Column(Time, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)

class Discount(Base):
    __tablename__ = 'discount'
    __table_args__ = (
        Index('idx_end_date', 'end_date')
    )

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    percent = Column(Numeric(precision=10, scale=5), default=0, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, default=datetime.utcnow, nullable=False)

class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        Index('idx_uuid', 'uuid'),
        Index('idx_email_timestamp', 'buyer_email', 'timestamp'),
    )

    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True, nullable=False)
    buyer_name = Column(String, nullable=False)
    buyer_email = Column(String, nullable=False)
    buyer_phone = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class Purchase(Base):
    __tablename__ ='purchase'

    id = Column(Integer, primary_key=True)
    price_id = Column(Integer, ForeignKey('price.id'), nullable=False)
    discount_id = Column(Integer, ForeignKey('discount.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

class Booking(Base):
    __tablename__ = 'booking'
    __table_args__ = (
        Index('idx_start_time', 'start_time'),
        Index('idx_purchase_id_start_time', 'purchase_id', 'start_time'),
    )

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    note = Column(String, nullable=True)