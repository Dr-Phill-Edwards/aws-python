import json
from jwt import (JWT, jwk_from_dict)
from jwt.exceptions import JWTDecodeError
import os
from tornado.httpclient import HTTPClient

instance = JWT()
public_keys = {}
public_key = None
messages = ["Messages"]

def message(event, context):
    body = get_post_data(event['body'])
    #result = verify(event['headers'])
    #if not bool(result):
    messages.append(body['message'])
    result = { 'statusCode': 200, 'body': json.dumps(messages) }
    return result

def get_post_data(body):
    postdata = {}
    for items in body.split('&'):
        values = items.split('=')
        postdata[values[0]] = values[1]
    return postdata

def verify(headers):
    result = {}
    if 'Authorization' in headers:
        token = headers['Authorization'].removeprefix('Bearer ')
        try:
            decoded = instance.decode(token, public_key, False)
        except JWTDecodeError:
            result = { 'statusCode': 403, 'body': 'Forbidden '}
    else:
        result = { 'statusCode': 401, 'body': 'Unauthorized '}
    return result

def get_keys():
    http_client = HTTPClient()
    uri = 'https://' + os.getenv('OKTA_DOMAIN') + '/oauth2/default/v1/keys'
    response = http_client.fetch(uri)
    jwks = json.loads(response.body)
    http_client.close()
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_key = jwk_from_dict(jwk)
        public_keys[kid] = public_key

#get_keys()
