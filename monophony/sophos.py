import requests
from collections import namedtuple as nt
from enum import Enum
import conf.config as c


'''
Sophos Central exposes 4 APIs.
The APIs and the specific arguments to build header, payload are defined here.
The API calls use Oauth v2.
'''


# Enumerate Sophos APIs and Endpoints
Api = Enum('Api', {'Common': 'common',
                   'Endpoint': 'endpoint',
                   'Organizaion': 'organization',
                   'Tenant': 'tenant',
                   'Tenants': 'tenants',
                   'Whoami': 'whoami'})

Common = Enum('Common', {'Alerts': 'common/v1/alerts',
                         'Users': 'common/v1/directory/users'})

Organization = Enum('Organization', {'Tenants': 'organization/v1/tenants'})


def rooturl():
    # TODO this is hardcoded and should be dynamic...
    return 'https://api-us03.central.sophos.com'

def tenant():
    return 'endpoint/v1/endpoints?pageSize=500'


# Hand tokens here
def jwt():
    '''
    Calls Sophos Oauth API and requests a JWT.
    Returns the JWT if request is granted.
    '''
    # TODO Encrypt JWT
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': c.SO_KEY,
        'client_secret': c.SO_SEC,
        'scope':  'token'
    }
    token = requests.post(
        'https://id.sophos.com/api/v2/oauth2/token',
        headers=header,
        data=payload).json()['access_token']

    return token


def headers(api, identity):
    return {'Authorization': 'Bearer {}'.format(jwt()),
            'X-{}-ID'.format(api): identity}


def whoami():
    globalurl = 'https://api.central.sophos.com'
    return requests.get(globalurl + '/whoami/v1',
                        headers={'Authorization': 'Bearer {}'.format(jwt())}
                        ).json()['id']


def tenants():
    '''
    Returns a dictionary containing tenant name as k,
    and namedtuple Tenant(id, apiHost) as v.
    '''
    # API host is currently not being used, but it could make for cleaner code.
    Tenant = nt('Tenant', ['id', 'apiHost'])
    response = requests.get('https://api.central.sophos.com/organization/v1/tenants',
                            headers=headers('Organization', whoami())
                            ).json()['items']

    def tenant(d):
        '''
        Takes a response and returns a named tuple.
        '''
        return Tenant(d['id'], d['apiHost'])

    return dict((d['name'], tenant(d)) for d in response)



