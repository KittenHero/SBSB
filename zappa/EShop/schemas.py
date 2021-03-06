import re
from datetime import datetime
from decimal import Decimal

from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    ValidationError,
    pre_load,
    post_load,
)
from django.utils.timezone import make_aware

from .models import (
    generate_token,
    EshopUser,
    Price,
    Discount,
    Purchase,
    Item
)

PHONE_PATTERN = re.compile('\+?\d{10,11}')


class EshopUserSchema(Schema):
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
        data['model'], _created = EshopUser.objects.update_or_create(
            email=data['email'],
            defaults={
                'name':data['name'],
                'phone':data['phone'],
            }
        )
        return data


class ItemSchema(Schema):
    massage_type = fields.Str(required=True)
    duration = fields.Time(required=True)
    discount = fields.Str(required=False)
    price = fields.Decimal(2, dump_only=True)
    net_price = fields.Decimal(2, dump_only=True)
    prices = {}
    discounts = {}

    @validates_schema
    def validate(self, data, **kwargs):
        massage, duration, code = data['massage_type'], data['duration'], data.get('discount')
        if (massage, duration) not in self.prices:
            price = Price.objects.filter(massage_type=massage, duration=duration, pk__in=Price.current_prices_pk).get()
            if not price:
                raise ValidationError('Item does not exists.')
            self.prices[massage, duration] = price

        if code not in self.discounts:
            discount = Discount.objects.filter(code=code, end_date__lt=make_aware(datetime.utcnow())).first()
            if discount:
                self.discounts[code] = discount

    @post_load
    def make_item(self, data, **kwargs):
        massage, duration, code = (
            data['massage_type'],
            data['duration'],
            data.get('discount'),
        )
        discount = self.discounts.get(code)
        if not discount: data.pop('discount', 0)
        model = Item(
            price=self.prices[massage, duration],
            discount=discount,
        )

        return dict(
            model=model,
            price=model.price.price,
            net_price=model.net_price,
            **data
        )


class PurchaseSchema(Schema):
    customer = fields.Nested(EshopUserSchema, required=False)
    token = fields.Str(required=False)
    items = fields.List(fields.Nested(ItemSchema, unknown='EXCLUDE'), required=True)
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
        customer = (
            data['customer']['model']
            if 'customer' in data else
            EshopUser.objects.get_or_create(
                email='test@sabaisabaithaimassage.com.au',
                defaults={ 'phone':'0000000000', 'name':'api' },
            )[0]
        )
        purchase = Purchase(
            user=customer,
            token=data.pop('token', None) or generate_token(),
        )
        models = [customer, purchase]
        total = 0
        for item in data['items']:
            item = item['model']
            total += item.net_price
            item.purchase = purchase
            models.append(item)

        return dict(models=models, token=purchase.token, total=total, **data)
