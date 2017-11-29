import functools

from flask import abort, request
import jose.jwt
import requests


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        pool_id = 'us-east-1_APXGoWFHh'
        region = 'us-east-1'
        response = requests.get(f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json")

        keys = {
            key['kid']: key
            for key in response.json().get('keys', [])
        }

        token = request.headers['idToken']

        try:
            header = jose.jwt.get_unverified_header(token)
        except jose.exceptions.JWTError:
            logging.debug('Could not parse JWT header')
            abort(403)

        key = keys[header['kid']]

        try:
            contents = jose.jwt.decode(token, key, audience='6o37c8db0u7l74o1nhukqaqdup')
        except jose.ExpiredSignatureError:
            logging.debug('Expired JWT signature')
            abort(403)

        if contents['iss'] != 'https://cognito-idp.us-east-1.amazonaws.com/us-east-1_APXGoWFHh':
            logging.debug('Issuing JWT source does not match')
            abort(403)

        if contents['token_use'] not in ['access', 'id']:
            logging.debug('Token use is not access nor id')
            abort(403)

        kwargs['user_email'] = contents['email']

        return f(*args, **kwargs)
    return decorated_function
