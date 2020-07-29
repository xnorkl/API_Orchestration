import requests
import namedtuple as nt
import conf.config as c


def so_jwt():
    '''
    Calls Sophos oauth api and requests a JWT.
    Returns the JWT if request is granted.
    '''
    # TODO Encrype JWT
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': c.SO_KEY,
        'client_secret': c.SO_SEC,
        'scope':  'token'
    }
    res = requests.post(
        'https://id.sophos.com/api/v2/oauth2/token',
        headers=header,
        data=payload).json()

    return res['access_token']


def so_tenant():
    jwt = so_jwt()
    return requests.get('https://api.central.sophos.com/whoami/v1',
                        headers={'Authorization': 'Bearer {}'.format(jwt)}
                        ).json()['id']


# TODO Move to Api.py
Token = nt('Token', ['id', 'jwt'])


def tokens():
    return Token(so_tenant(), so_jwt())
