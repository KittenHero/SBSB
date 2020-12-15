import re
from datetime import datetime
from decimal import Decimal
import uuid

from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    ValidationError,
    pre_load,
    post_load,
)

from models import (
    session,
    Customer,
    Price,
    Discount,
    Purchase,
)

PHONE_PATTERN = re.compile('\+?\d{10,11}')
UUID_NAMESPACE = uuid.uuid3(uuid.NAMESPACE_DNS, 'sabaisabaithaimassage.com.au')


class CustomerSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)

    @pre_load
    def remove_spaces(self, data, **kwargs):
        data['email'] = data['email'].strip()
        data['phone'] = data['phone'].replace(' ', '')
        return data

    @validates('phone')
    def validate_phone(self, data, **kwargs):
        if not PHONE_PATTERN.fullmatch(data):
            raise ValidationError('Invalid Phone Number')

    @post_load
    def make_customer(self, data, **kwargs):
        data['model'] = Customer(
            uuid=uuid.uuid3(
                UUID_NAMESPACE,
                data['email'] + datetime.utcnow().isoformat()
            ),
            buyer_name=data['name'],
            buyer_email=data['email'],
            buyer_phone=data['phone'],
        )
        return data


class ItemSchema(Schema):
    massage_type = fields.Str(required=True)
    duration = fields.Time(required=True)
    amount = fields.Int(missing=1)
    discount = fields.Str(required=False)
    price_per = fields.Decimal(2, dump_only=True)
    price_gross = fields.Decimal(2, dump_only=True)
    discount_amount = fields.Decimal(2, dump_only=True)
    net_price = fields.Decimal(2, dump_only=True)
    prices = {}
    discounts = {}

    @validates_schema
    def validate(self, data, **kwargs):
        massage, duration, code = data['massage_type'], data['duration'], data.get('discount')
        price = session.query(Price).filter_by(
            massage_type=massage,
            duration=duration
        ).order_by(Price.start_date.desc()).first()
        if not price:
            raise ValidationError('Item does not exists.')

        discount = session.query(Discount).filter(
            Discount.code == code,
            Discount.end_date > datetime.utcnow(),
        ).first()
        if code and not discount:
            raise ValidationError('Discount not valid', 'discount')

        self.prices[massage, duration] = price
        self.discounts[code] = discount

    @post_load
    def make_purchase(self, data, **kwargs):
        massage, duration, code, amount = (
            data['massage_type'],
            data['duration'],
            data.get('discount'),
            data['amount']
        )
        discount = self.discounts.get(code)
        model = Purchase(
            amount=amount,
            price=self.prices[massage, duration],
            discount=discount,
        )
        price_per = model.price.price
        price_gross = model.amount * price_per
        discount_amount = min(
            price_gross * discount.percent * Decimal('0.01'),
            discount.per_item * amount,
            price_gross
        ) if discount else 0
        net_price = price_gross - discount_amount

        return dict(
            model=model,
            price_per=price_per,
            price_gross=price_gross,
            discount_amount=discount_amount,
            net_price=net_price,
            **data
        )



class PurchaseSchema(Schema):
    customer = fields.Nested(CustomerSchema, required=True)
    items = fields.List(fields.Nested(ItemSchema), required=True)
    total = fields.Decimal(2, dump_only=True)
    payment_token = fields.Str(required=False)
    payment_status = fields.Str(required=False, dump_only=True)
    payment_response = fields.Dict(required=False, dump_only=True)

    @validates('items')
    def validate_items(self, data, **kwargs):
        if len(data) < 1:
            raise ValidationError('Must have at least 1 item')

    @post_load
    def connect_models(self, data, **kwargs):
        customer = data['customer']['model']
        models = [customer]
        total = 0
        for item in data['items']:
            purchase = item['model']
            total += item['net_price']
            purchase.customer = customer
            models.append(purchase)

        return dict(models=models, total=total, **data)
