import requests
import json
from functools import partial

import config
import pp
from enums import app,siemendpoint, peopleendpoint

# Higher Order Functions

def isiterable(obj):
    """ Check if an object is iterable. If not, ask forgiveness. """
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True


def member(a,b):
    """ Takes a value a & returns if a is an element of b. """
    if a in set(elem.value for elem in b):
        return a
    else:
        raise TypeError('{} is not a member of {}'.format(a,b))


def evoke(m, o):
    """ Takes a string m and o, & returns a matching object in module m by name. """
    return getattr(globals()[m], o)


def ismember(m, f, a):
    """ Take a function f(args) in module m & return True or False. """
    if member(f, evoke(m, a)):
        return True
    else:
        return False


def helper(f, args):
    """ Helper fucntion that takes a function f and an object args and returns f(args).

    Helper tries to determine first how to unpack if args are an iterable.
    If args are not iterable, helper casts args to list to then unpack.
    This allows for avoiding passing a single argument as an iterable.

    """
    try:
        if callable(f):
            if isinstance(args, list) or isinstance(args, tuple):
                return f(*args)
            if isinstance(args, dict):
                return f(**args)
        else:
             return f(args)
    except Exception as e:
        print(e)


def call(m, f, *args):
    """ Takes a module, function, and *args & returns f(*args). """
    return helper(evoke(m, f), *args)

# API Functions

#Redude arity of higher order functions.
enumapi = partial(ismember, a='Api')
rooturl = partial(evoke, o='rooturl') #Why can't this be done with a call?


def evoke_api(m, f, *args):
    """ Takes a function f(args) of module m & returns f() if f is an api in m. """
    if enumapi(m, f):
        return call(m, f, args)


def buildurl(m, p, q):
    """ Take a root r and leafs l, q & return str(r/l/q). """
    return '/'.join((rooturl(m)(), p, q))


def get(app, api, endpoint, *args):
    """ Takes an app, api, and args (where needed). Returns a GET request.

    Parameters
    ----------
    app: str
      The application name. Use app.<Name>.value if string is not known.
    api: str
      The api name for a given application.
      Use <app>.Api.value if string is not known.
    endpoint: str
      The endpoint of a given api.
      Use <app>.<Name>.<Endpoint>.value

    """
    return requests.get(
        buildurl(app, api, endpoint),
        params=call(app, api, args),
        auth=(config.PP_KEY, config.PP_SEC)
    )

"""
Data Flow
    get('pp', 'people', 'vap', 14)
        1) buildurl('pp', 'people', 'vap')
            buildurl(rooturl('pp')(), 'people', 'vap')
                buildurl(evoke('pp', rooturl)(), 'people', 'vap')
                    buildurl(pp.rooturl(), 'people', 'vap')
        > returns: https://tap-api-v2.proofpoint.com/v2/people/vap

    get('pp', 'siem', 'all')
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
