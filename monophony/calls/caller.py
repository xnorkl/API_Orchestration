import config
import requests
from datetime import datetime as dt, timedelta
from enums import app,siemendpoint, peopleendpoint
import pp

# Generate appropriate timespans.
def timespan(s):
    ''' Return a timedelta of 1 hours from now. '''
    return dt.utcnow() - timedelta(seconds=s)


def isoformat(d):
    ''' Take a delta t and output t as ISO 8601. '''
    return d.replace(microsecond=0).isoformat() + 'Z'


def lasthour():
    return isoformat(timespan(3600))


# Query and Generate API payloads
def member(a,b):
    ''' Takes a value a & returns if a is an element of b. '''
    if a in set(elem.value for elem in b):
        return a


def evoke(m, o):
    ''' Takes a string m and o, & returns a matching object in module m by name. '''
    return getattr(globals()[m], o)


def evoke_api(m, f, a):
    ''' Takes a function f of module m & returns f() if f is an api in m. '''
    if member(f, evoke(m, 'Api')):
        return evoke(m, f)(*a)


def buildurl(m, p, q):
    ''' Take a root r and leafs l, q & return str(r/l/q) '''
    return '/'.join((evoke(m,'rooturl')(), p, q))


def get(app, api, endpoint, args):
    ''' Request takes a payload p for a given api and returns a get request. '''
    return requests.get(
        buildurl(app, api, endpoint),
        params=evoke_api(app, api, args),
        auth=(config.PP_KEY, config.PP_SEC)
    ).text

# Create Requests
# Arguments can be passed in the form of tuples, dicts, or directly, etc...
# Very Attacked People
# TODO this will have a command structure...
vap_args = {
            'app': 'pp',
            'api': 'people',
            'endpoint': 'vap',
            'args': ()
            }

# Clickes Blocked
options = (lasthour(), 'active')
cb_args = (app.PP.value, pp.Api.SIEM.value, siemendpoint.Clicksblocked.value, options)

# Messages Blocked
mb_args = (app.PP.value, pp.Api.SIEM.value, siemendpoint.Messagesblocked.value, options)


#print(get(**vap_args))
print(get(*cb_args))
print(get(*mb_args))

