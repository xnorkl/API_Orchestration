import conf.config as config
from helper import call, ismember, evoke
import requests
from functools import partial


# API Functions


# Redude arity of these helper functions.
enumapi = partial(ismember, a='Api')
rooturl = partial(evoke, o='rooturl')


def evoke_api(m, f, *args):
    """
    Takes a function f module m and args of f.
    Returns f(args) if f is an api in m.
    """
    if enumapi(m, f):
        return call(m, f, args)


def buildurl(m, p, q):
    """ Take a root r and leafs l, q & return str(r/l/q). """
    return '/'.join((rooturl(m)(), p, q))


def url(m, p=[]):
    """
    Improved on buildurl. Takes a rooturl and a list of non-empty strings.
    """
    return '/'.join((rooturl(m)(), *list(filter(None, p))))


def get(app, api, endpoint, *args, tenant=None):
    """
    Takes an app, api, and args (where needed). Returns a GET request.

    Parameters
    ----------
    app: str
      The application name. Use app.<Name>.value if string is not known.
    api: str:
      The api name for a given application.
      Use <app>.Api.value if string is not known.
    endpoint: str
      The endpoint of a given api.
      Use <app>.<Name>.<Endpoint>.value
    """

    if tenant:
        return requests.get(
            url(app, [api, endpoint]),
            headers=evoke(app, 'headers')(api, tenant))
    return requests.get(
        url(app, [api, endpoint]),
        params=call(app, api, args),
        auth=(config.PP_KEY, config.PP_SEC))


def post(app, payload):
    return requests.post(
        url(app),
        data=payload)


"""
Unpacking the get function...

    ex. get('pp', 'people', 'vap', 14)
        1) buildurl('pp', 'people', 'vap')
            buildurl(rooturl('pp')(), 'people', 'vap')
                buildurl(evoke('pp', rooturl)(), 'people', 'vap')
                    buildurl(pp.rooturl(), 'people', 'vap')
        > returns: https://tap-api-v2.proofpoint.com/v2/people/vap

    ex. get('pp', 'siem', 'all')
        2) call('pp','siem')
            helper(evoke('pp', 'siem'))
                helper('siem')
                    siem()
        > returns: {
                    'format': 'json',
                    'sinceTime': '2020-07-09T15:13:53Z',
                    'threatType': 'url',
                    'threatStatus': 'active'
                    }
"""
