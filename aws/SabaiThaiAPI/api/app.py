import os
import json

import boto3
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from models import session
from schema import PurchaseSchema
from securepay import secure_pay_client


ses = boto3.client('ses', region_name='ap-southeast-2')

DEFAULT_DESTINATION = os.environ.get('EMAIL_TO')
EMAIL_FROM = os.environ.get('EMAIL_FROM')


def send_email(event, context):
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    try:
        body = json.loads(event.get('body'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': 'Invalid JSON'
        }
    if not ('subject' in body and 'text' in body):
        return {
            'statusCode': 400,
            'body': 'Missing subject or text'
        }

    ses.send_email(
        Destination={'ToAddresses': body.get('to', [DEFAULT_DESTINATION])},
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
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Access-Control-Allow-Credentials" : True # Required for cookies, authorization headers with HTTPS
        },
        'body': "{}"
    }


def purchase(event, context):
    try:
        body = json.loads(event.get('body'))
        purchases = PurchaseSchema().load(body)
        session.add_all(purchases['models'])
        if not purchases.get('payment_token'):
            session.flush()
            return {
                'statusCode': 200,
                'body': json.dumps(PurchaseSchema().dump(purchases))
            }
        payment = secure_pay_client.make_payment(
            amount=purchases['total'],
            token=purchases['payment_token'],
            ip=event['requestContext']['identity']['sourceIp'],
            uuid=purchases['customer']['uuid'],
        )
        session.add(payment)
        session.commit()
        purchases.update(payment_status=payment.status, payment_response=payment.response)
        return {
            'statusCode': 200,
            'body': json.dumps(PurchaseSchema().dump(purchases))
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': 'Invalid JSON'
        }
    except ValidationError as err:
        return {
            'statusCode': 400,
            'body': json.dumps(err.messages)
        }
    except SQLAlchemyError as e:
        session.rollback()
        return {
            'statusCode': 500,
            'body': str(e.orig)
        }

