import sys
import datetime
import configparser
from enum import Enum
import json
import requests
import pprint
import re
import hashlib
from abc import ABC, abstractmethod
from Config import *


def delta_t():
    ''' Return last hour in ISO 8601 format. '''

    now = datetime.datetime.utcnow()
    min_delta = now - datetime.timedelta(seconds=3600)
    return min_delta.replace(microsecond=0).isoformat() + 'Z'

class API_Block():

    def __init__(self, index, stamp, stash, phash):
        self.index = index
        self.stamp = stamp
        self.stash = stash
        self.phash = phash
        self.hash = self.hash()

    def hash(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.stamp).encode('utf-8'))
        key.update(str(self.stash).encode('utf-8'))
        key.update(str(self.phash).encode('utf-8'))
        return key.hexdigest()


class API(ABC):
    ''' An Abstract API class '''

    def __init__(self):
        self.interval = delta_t()
        super().__init__()

    @abstractmethod
    def credentials(self):
        pass

class Proofpoint(API):
    '''Proofpoint API request. Returns JSON output. '''

    def __init__(self):
        self.url = PP_URL
        self.creds = self.credentials()
        super().__init__()

    def credentials(self):
        return (PP_KEY,PP_SEC)

    # Enumerate calls for the siem api.
    siem_call = Enum(
        'siem_call',
        'clicks_blocked clicks_permitted messages_blocked messages_delivered issues everything'
    )

    ## Generate API Payloads #

    @classmethod
    def siem(cls, call):
        ''' Defines a payload provided by the SIEM API. Returns JSON '''

        # Create Class Instance
        self = cls()
        url   = self.url
        delta = self.interval
        creds = self.creds

        siem_payload = {
            'format': 'json',
            'sinceTime': delta ,
            'threatStatus': ['active', 'cleared']
        }

        if call is self.siem_call.clicks_blocked:
            url = url + 'clicks/blocked'
        elif call is self.siem_call.clicks_permitted:
            url = url + 'clicks/permitted'
        elif call is self.siem_call.messages_blocked:
            url = url + 'messages/blocked'
        elif call is self.siem_call.messages_delivered:
            url = url + 'messages/delivered'
        elif call is self.siem_call.issues:
            url = url + 'issues'
        elif call is self.siem_call.everything:
            url = url + 'all'
        else:
            raise TypeError('call must be an instance of siem_call enum') # Redundancy

        # Invoke HTML GET Request with the construscted payload.
        siem_r = requests.get(url,params=siem_payload,auth=creds)

        return siem_r.json()

    @classmethod
    def forensics(cls, creds):
        ''' Defines a payload provided by the Forensics API. Returns JSON '''

        forensics_payload = {
            'threatId': '671814f49dce70230831baa15a2cf8991d5194d9e05a1ff2266349b593c1dd67'
        }

        forensics_r = requests.get(
            'https://tap-api-v2.proofpoint.com/v2/forensics',
            params=forensics_payload,
            auth=(PRINCIPAL, SECRET)
        )
        return forensics_r.json()

    @classmethod
    def people(cls, creds):
        ''' Defines a payload provided by the Poeple API. Returns JSON.'''

        people_payload = {'window': 90}

        people_r = requests.get(
            'https://tap-api-v2.proofpoint.com/v2/people/vap',
            params=people_payload,
            auth=(PRINCIPAL, SECRET)
        )
        return siem_r.json()

    ## Create Reports from API Requests ##

    @staticmethod
    def blocklist(pp):
        ''' Defines a Blocklist. Returns a List of formatted Text '''
        #TODO: Add more checks.
        T = last_hour()
        CALL = siem_call.messages_blocked
        blocked = pp.siem(CREDS, URL, CALL, T)
        for report in blocked['messagesBlocked']:
            if report['fromAddress'][0] != report['toAddresses'][0]:
                m = re.search(
                    r"[a-zA-Z0-9_\-\.]+@[a-zAA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}",
                    report['headerFrom']
                )
                if m:
                    from_addr = m[0]
                else:
                    from_addr = "None"
                to_addr = [a for a in report['toAddresses']]
                d = {
                    'from': from_addr,
                    'to': to_addr,
                    'sender IP': report['senderIP'],
                    'threat': report['threatsInfoMap'][0]['threat'],
                    'threatID': report['threatsInfoMap'][0]['threatID']
                }
            return [ "{} : {}".format(k, v) for k, v in d.items()]

    @staticmethod
    def vap(pp):
        people_reports = people_r.json()
        for user in people_reports['users']:
            return user['identity']['emails'][0]


pp = Proofpoint()
call = pp.siem_call.everything
report = pp.siem(call)

print(report)
#       answer = str(report['fromAddress'][0]) + '\n'
#       with open("blocklist.txt", 'a') as outfile:
#           outfile.write(answer)


# If we want to store JSON, then we can do this...

# Write to and output
# responses=[siem_r.json(),forensics_r.json()]
# stores=['siem.json','forensics.json']
#i = 0
# for response in responses:
#    with open(stores[i], 'a') as outfile:
#        json.dump(response, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
#    i = i + 1
