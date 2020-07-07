import config
import requests
from datetime import datetime as dt, timedelta
from enums import app,siemendpoint, peopleendpoint
import pp

# Generate appropriate timespans.
def timespan(s):
    """ Return a timedelta of 1 hours from now. """
    return dt.utcnow() - timedelta(seconds=s)


def isoformat(d):
    """ Take a delta t and output t as ISO 8601. """
    return d.replace(microsecond=0).isoformat() + 'Z'


def lasthour():
    return isoformat(timespan(3600))


# Query and Generate API payloads
def isiterable(obj):
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


def evoke(m, o):
    """ Takes a string m and o, & returns a matching object in module m by name. """
    return getattr(globals()[m], o)


def evoke_api(m, f, a):
    """ Takes a function f of module m & returns f() if f is an api in m. """
    if member(f, evoke(m, 'Api')):
      if isiterable(a):
        return evoke(m, f)(*a)
      else:
        try:
          return evoke_api(m, f, [a])
        except:
          raise TypeError('args a must be an iterable.')



def buildurl(m, p, q):
    """ Take a root r and leafs l, q & return str(r/l/q). """
    return '/'.join((evoke(m,'rooturl')(), p, q))


def get(app, api, endpoint, args):
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
        params=evoke_api(app, api, args),
        auth=(config.PP_KEY, config.PP_SEC)
    ).text #TODO move .text and wrap in other function

# Create Requests
# Arguments can be passed in the form of tuples, dicts, or directly, etc...
# Very Attacked People
# TODO this will have a command structure...
def helper(f, args):
  if isinstance(args, list):
      return f(*args)
  elif isinstance(args, dict):
      return f(**args)
  else:
    try:
      #TODO should work with evoke(m,f)(a) when 
      print('trying...')
      return f(*list(args))
    except:
      print(type(args))
      raise TypeError('Collection C must be an iterable.')

# TODO with helper function and get, build common api commands.
vap_args = {
            'app': 'pp',
            'api': 'people',
            'endpoint': 'vap',
            'args': 90
            }

# Clickes Blocked
options = (lasthour(), 'active')
cb_args = (app.PP.value, pp.Api.SIEM.value, siemendpoint.Clicksblocked.value, options)

# Messages Blocked
mb_args = (app.PP.value, pp.Api.SIEM.value, siemendpoint.Messagesblocked.value, options)

print(helper(get,vap_args))
#print(get(**vap_args))
#print(get(*cb_args))
#print(get(*mb_args))
print(pp.SIEM.Clicksblocked.value)


