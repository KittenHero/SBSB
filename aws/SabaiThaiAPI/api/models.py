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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine(os.environ.get('DB_ENGINE', 'postgres://admin@localhost/SabaiThaiDB'))
session = sessionmaker(engine)()

Base = declarative_base(metadata=MetaData(schema='sabai_thai'))


class Price(Base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    massage_type = Column(String, nullable=False)
    duration = Column(Time, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_type_duration_date', massage_type, duration, start_date),
    )

class Discount(Base):
    __tablename__ = 'discount'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    per_item = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    percent = Column(Numeric(precision=10, scale=5), default=0, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_code_end_date', code, end_date),
    )

# TODO: DiscountValid Table shows which Discount applies to which Price

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True, nullable=False)
    buyer_name = Column(String, nullable=False)
    buyer_email = Column(String, nullable=False)
    buyer_phone = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    purchases = relationship('Purchase', back_populates='customer')
    payments = relationship('Payment', back_populates='customer')

    __table_args__ = (
        Index('idx_uuid', uuid),
        Index('idx_email_timestamp', buyer_email, timestamp),
    )

class Purchase(Base):
    __tablename__ ='purchase'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, default=1, nullable=False)
    price_id = Column(Integer, ForeignKey('price.id'), nullable=False)
    discount_id = Column(Integer, ForeignKey('discount.id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    customer = relationship('Customer', back_populates='purchases')
    price = relationship('Price')
    discount = relationship('Discount')
    booking = relationship('Booking')

    __table_args__ = (
        Index('idx_customer_id', customer_id),
    )


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    note = Column(String, nullable=True)

    __table_args__ = (
        Index('idx_start_time', start_time),
        Index('idx_purchase_id_start_time', purchase_id, start_time),
    )


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    currency = Column(String(3), nullable=False)
    status = Column(String(10), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    orderId = Column(String, ForeignKey('customer.uuid'), nullable=False)
    gatewayResponseCode = Column(String(2), nullable=True)
    errorCode = Column(String(3), nullable=True)
    response = Column(JSONB, nullable=False)

    customer = relationship('Customer', back_populates='payments')

    __table_args__ = (
        Index('idx_orderId', orderId),
    )
