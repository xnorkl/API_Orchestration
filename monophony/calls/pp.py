import config
from datetime import datetime as dt, timedelta
from enum import Enum
import os
import re
import requests

# Enumerate Proofpoint APIs and API calls.
# Enumerators are used similar to Haskell records.
Api = Enum('Api',
           {'SIEM':'siem',
            'People':'people',
            'Foresnics': 'forensics',
            'Campaign': 'campaign'
            }
           )


def rooturl():
    return 'https://tap-api-v2.proofpoint.com/v2'


def siem(t,s):
    ''' Returns a payload for the SIEM API. '''
    return {
                'format': 'json',
                'sinceTime': t,
                'threatStatus': s
    }


def people():
    ''' Returns a Payload for the people API. '''
    return {'window': 90}


def forensics():
    ''' Returns a Payload for the forensics API. '''
    return {'threatId': get_threatid() }


def campaign():
    ''' Returns a campaign ID. '''
    return get_campaignid()


