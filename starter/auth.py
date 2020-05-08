import json
import os
from urllib.request import urlopen
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'udacity-capstone-project.auth0.com')
ALGORITHMS = os.environ.get('ALGORITHMS', 'RS256')
API_AUDIENCE = os.environ.get('API_AUDIENCE', 'capstone-app')

# AUTH0_DOMAIN = 'udacity-capstone-project.auth0.com'
# ALGORITHMS = ['RS256']
# API_AUDIENCE = 'capstone-app'

# print(AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE)

# AUTH0_DOMAIN = 'dxpr.auth0.com'
# ALGORITHMS = 'RS256'
# API_AUDIENCE = 'agency'


class AuthError(Exception):

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    '''
    Implementing get_token_auth_header method
    - It gets header from request
    - Split the token from header
    - return the token part when called
    '''
    auth = request.headers.get('Authorization', None)
    # if token is missing raise error
    if auth is None:
        raise AuthError({
            'code': 'no_auth_header',
            'description': 'auth header is needed'
        }, 401)
    # spliting the auth token
    parts = auth.split(' ')
    # checking if token is a bearer token
    if parts[0] != 'Bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Auth header doesn\'t have Bearer at starting'
        }, 401)
    # checking if token is available
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)
    token = parts[1]
    return token


def check_permissions(permission, payload):
    '''
    Implementing check_permissions methos
    @ Input :- permission: string having permissions (i.e. add:actor)
               payload: decoded jwt token
    -Raise error if permission is not included in payload
    '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'JWT don\'t have this permissions'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'access_forbidden',
            'description': 'Access Forbidden'
        }, 401)
    return True


def verify_decode_jwt(token):
    '''
    Implement verify_decode_jwt(token) method
        @INPUTS
            token: a json web token (string)
        - It should be an Auth0 token with key id (kid)
        - It should verify the token using Auth0 /.well-known/jwks.json
        - It should decode the payload from the token
        - It should validate the claims
        - return the decoded payload
    '''
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. '
                               'Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
