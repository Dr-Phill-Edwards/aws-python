import base64
import json
from jwt import (JWT, jwk_from_dict)
from jwt.exceptions import JWTDecodeError
import os

instance = JWT()
public_keys = {}
public_key = None
messages = ["Messages"]

def message(event, context):
    body = get_post_data(event['body'])
    result = verify(body['token'])
    if not bool(result):
        messages.append(body['message'])
        result = { 
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            },
            'body': json.dumps(messages) 
    }
    return result

def get_post_data(body):
    postdata = {}
    for items in body.split('&'):
        values = items.split('=')
        postdata[values[0]] = values[1]
    return postdata

def verify(token):
    result = {}
    try:
        decoded = instance.decode(token, public_key, False)
    except JWTDecodeError:
        result = { 'statusCode': 403, 'body': 'Forbidden '}
    return result

def get_keys():
    keys = base64.b64decode(os.environ['OKTA_KEYS'])
    jwks = json.loads(keys)
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_key = jwk_from_dict(jwk)
        public_keys[kid] = public_key

get_keys()