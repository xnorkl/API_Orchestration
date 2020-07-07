import config
from datetime import datetime as dt, timedelta
from enum import Enum
import os
import re
import requests

# Enumerate Proofpoint APIs and API calls.
# Enumerators are used similar to Haskell records.
# These may be removed for tuples or dicts...
Api = Enum('Api',
    {
      'SIEM':'siem',
      'People':'people',
      'Foresnics': 'forensics',
      'Campaign': 'campaign'
      }
    )


SIEM = Enum('SIEM',
    {
      'Clicksblocked': 'clicks/blocked',
      'Clickspermitted': 'clicks/permitted',
      'Messagesblocked': 'messages/blocked',
      'Messagesdelivered': 'messages/delivered',
      'Issues': 'issues',
      'Everything': 'all'
      }
    )

#TODO Finish adding Enums for all API Endpoints.

def rooturl():
    return 'https://tap-api-v2.proofpoint.com/v2'


def siem(t,s):
    """ Returns a payload for the SIEM API. 

    Parameters
    ----------

    t: time duration in ISO 8601 format
      To date, Proofpoint SIEM API only accepts 3600s (1 hour)...
    s: str

    """
    #TODO list s options 
    return {
        'format': 'json',
        'sinceTime': t,
        'threatStatus': s
        }


def people(n):
    """ Takes an n-many days, returns a Payload for the people API. """
    return {'window': n}


def forensics():
    """ Returns a Payload for the forensics API. """
    return {'threatId': get_threatid() }


def campaign():
    """ Returns a campaign ID. """
    return get_campaignid()


