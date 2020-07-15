from datetime import datetime as dt, timedelta

# Generate appropriate timespans.
def timespan(s):
    """ Return a timedelta of 1 hours from now. """
    return dt.utcnow() - timedelta(seconds=s)


def isoformat(d):
    """ Take a delta t and output t as ISO 8601. """
    return d.replace(microsecond=0).isoformat() + 'Z'


def lasthour():
    return isoformat(timespan(3600))
