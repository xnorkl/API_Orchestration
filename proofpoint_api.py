import sys
import datetime
import config
import configparser
from enum import Enum
import json
import requests
import pprint
import re
import hashlib


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



class API(object):
    ''' Here to access methods needed accross API classes '''
    def __init__(self):
        self.last_hour = self.last_hour()

    def last_hour(self):
        ''' Return last hour in ISO 8601 format. '''

        now = datetime.datetime.utcnow()
        min_delta = now - datetime.timedelta(seconds=3600)
        return min_delta.replace(microsecond=0).isoformat() + 'Z'


class Proofpoint(API):
    '''Proofpoint API request. Returns JSON output. '''

    ## Class Variables ##
    #
    T   = API().last_hour
    # Root URL for all Proofpoint API calls.
    URL = 'https://tap-api-v2.proofpoint.com/v2/siem/'
    # Credentials are generated at the TAP server.
    PRINCIPAL   = "a737f3cb-8c8e-d873-086b-270540dcab5d"
    SECRET      = "f298519077c461d214e9b615e8c3515e35f5b1079a73c90f62caacf9ddacddf0"
    CREDS       = (PRINCIPAL, SECRET)

    ## Generate API Payloads ##
    # Enumerate calls for the siem api.
    siem_call = Enum(
        'siem_call',
        'clicks_blocked clicks_permitted messages_blocked messages_delivered issues all'
    )

    def siem(call, delta_t=T, creds=CREDS, url=URL):
        ''' Defines a payload provided by the SIEM API. Returns JSON '''
        # Handle enum types:
        #if not isinstance(call, siem_call):
        #    raise TypeError('call must be an instance of siem_call enum')

        siem_payload = {
            'format': 'json',
            'sinceTime': delta_t,
            'threatStatus': ['active', 'cleared']
        }

        if call is clicks_blocked:
            url = url + 'clicks/blocked'
        elif call == 'clicks_permitted':
            url = url + 'clicks/permitted'
        elif call == 'messages_blocked':
            url = url + 'messages/blocked'
        elif call == 'messages_delivered':
            url = url + 'messages/delivered'
        elif call == 'issues':
            url = url + 'issues'
        elif call == 'all':
            url = url + 'all'
        else:
            raise TypeError('call must be an instance of siem_call enum') # Redundancy

        # Invoke HTML GET Request with the construscted payload.
        siem_r = requests.get(url,params=siem_payload,auth=creds)

        return siem_r.json()

    def forensics(creds):
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

    def people(creds):
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


CALL = Proofpoint.siem_call.messages_blocked
pp = Proofpoint()

pp.siem(CALL)

print(pp)
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
