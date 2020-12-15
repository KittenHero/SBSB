from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
import os

from requests import Session
from marshmallow import (
    Schema,
    fields,
    post_load,
)

from models import (
    Base,
    Customer,
    Payment,
)


class Client:

    def __init__(
                self,
                client=os.environ.get('SECUREPAY_CLIENT'),
                secret=os.environ.get('SECUREPAY_SECRET'),
                merchant_code=os.environ.get('SECUREPAY_MERCHANT'),
                auth_url=os.environ.get(
                    'SECUREPAY_AUTH',
                    'https://hello.sandbox.auspost.com.au/oauth2/ausujjr7T0v0TTilk3l5/v1/token'
                ),
                payment_url=os.environ.get(
                    'SECUREPAY_PAYMENT',
                    'https://payments-stest.npe.aupost.zone/v2/payments'
                ),
        ):
        self.session = Session()
        self.client_id = client
        self.secret = secret
        self.merchant_code = merchant_code
        self.auth_url = auth_url
        self.payment_url = payment_url

    @property
    def auth(self):
        if not self._auth or self._auth.expired:
            r = self.session.post(
                self.auth_url,
                auth=(self.client_id, self.secret),
                data={
                    'grant_type': 'client_credentials',
                    'scope': ' '.join([
                        'https://api.payments.auspost.com.au/payhive/payments/read',
                        'https://api.payments.auspost.com.au/payhive/payments/write',
                        'https://api.payments.auspost.com.au/payhive/payment-instruments/read',
                        'https://api.payments.auspost.com.au/payhive/payment-instruments/write',
                    ])
                },
            )
            self._auth = AuthSchema().load(r.json())

        return self._auth.access_token

    def make_payment(self, amount, token, ip, uuid):
        r = self.session.post(
            self.payment_url,
            json={
                'amount': amount,
                'merchantCode': merchant_code,
                'token': token,
                'ip': ip,
                'orderId': uuid,
            },
            headers={
                'Idempotency-Key': uuid,
                'Authorization': f'Bearer {self.auth}'
            }
        )
        payment = PaymentSchema().load(r.json())
        return payment



@dataclass
class Auth:
    access_token: str
    token_type: str
    expires_in: timedelta
    scope: str
    expires_at: datetime = field(init=False)

    def __post_init__(self):
        self.expires_at = datetime.utcnow() + self.expires_in

    @property
    def expired(self):
        return datetime.utcnow() > self.expires_at


class AuthSchema(Schema):
    access_token = fields.Str()
    token_type = fields.Str()
    expires_in = fields.TimeDelta()
    scope = fields.Str()

    @post_load
    def load_auth(self, data, **kwargs):
        return Auth(**data)


class PaymentSchema(Schema):
    createdAt = fields.DateTime()
    merchantCode = fields.Str()
    customerCode = fields.Str()
    token = fields.Str()
    ip = fields.IPv4()
    amount = fields.Decimal()
    currency = fields.Str()
    status = fields.Str()
    orderId = fields.UUID()
    bankTransactionId = fields.Str()
    gatewayResponseCode = fields.Str()
    errorCode = fields.Str(required=False)

    @post_load
    def load_model(self, data, **kwargs):
        return Payment(**data, response=data)


secure_pay_client = Client()
