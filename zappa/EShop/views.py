from datetime import datetime, timedelta
import os
import json

import boto3
from marshmallow import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .schemas import PurchaseSchema
from .securepay import secure_pay_client

ses = boto3.client('ses', region_name='ap-southeast-2')

DEFAULT_DESTINATION = os.environ.get('EMAIL_TO', '').split(' ')
EMAIL_FROM = os.environ.get('EMAIL_FROM')


def api(allowed_methods=[]):
    def wrapper(func):
        @csrf_exempt
        def wrapped(request, *args, **kwargs):
            if request.method not in allowed_methods:
                return HttpResponseNotAllowed(allowed_methods)
            try:
                with transaction.atomic():
                    ret = func(request, *args, **kwargs)
                if not ret:
                    response = HttpResponse()
                elif isinstance(ret, dict):
                    response = JsonResponse(ret)
                elif isinstance(ret, str):
                    response = HttpResponse(ret)
            except json.JSONDecodeError:
                response = HttpResponse('Invalid JSON', status=400)
            except ValidationError as err:
                response = JsonResponse(err.messages, status=400)
            except IntegrityError as err:
                response = HttpResponse(err, status=500)
            except ValueError as err:
                response = HttpResponse(err, status=400)
            return response

        return wrapped
    return wrapper


@api(['GET', 'POST'])
def blank(request):
    return {}


@api(['POST'])
def contact(request):
    body = json.loads(request.body)
    if not ('subject' in body and 'text' in body):
        raise ValueError('Missing subject or text')

    ses.send_email(
        Destination={'ToAddresses': body.get('to', DEFAULT_DESTINATION)},
        Message={
            'Subject': { 'Data': body['subject'] },
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': body.get('html', body['text']),
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body['text'],
                },
            }
        },
        Source=EMAIL_FROM
    )

@api(['POST'])
def purchase(request):
    body = json.loads(request.body)
    purchases = PurchaseSchema().load(body)

    if not purchases.get('payment_token'):
        return PurchaseSchema().dump(purchases)

    for m in purchases['models']:
        m.save()
    customer, purchase, *_ = purchases['models']

    ip = request.META.get(
        'HTTP_X_FORWARDED_FOR',
        request.META.get('REMOTE_ADDR', '')
    ).split(',')[0].strip()
    payment = secure_pay_client.make_payment(
            amount=f'{purchases["total"]:.2f}',
        token=purchases['payment_token'],
        ip=ip,
        uuid=purchase.token,
    )
    payment.save()
    purchases['models'][1].save()
    purchases.update(payment_status=payment.status, payment_response=payment.response)
    return PurchaseSchema().dump(purchases)
