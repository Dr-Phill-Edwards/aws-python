import json
from jwt import (JWT, jwk_from_dict)
import os
from tornado.httpclient import HTTPClient

public_keys = {}
messages = ["Messages"]

def message(event, context):
    return json.dumps(messages)

def get_keys():
    http_client = HTTPClient()
    uri = 'https://' + os.getenv('OKTA_DOMAIN') + '/oauth2/default/v1/keys'
    response = http_client.fetch(uri)
    jwks = json.loads(response.body)
    http_client.close()
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwk_from_dict(jwk)
        
    print(public_keys)

get_keys()
